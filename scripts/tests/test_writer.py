"""
Tests for scripts/writer.py, written test-first against the interface
designed during the candidate #2 architecture-review grilling session.

writer.py is the thin adapter that walks an already parsed/resolved/fixed-up
Page tree (see scripts/tree.py) and does the actual disk I/O: writing Hugo
content files and copying referenced images. It intentionally knows nothing
about markdown parsing, cross-reference resolution, or text fixups -- those
are all baked into the Page tree's content by the time write_tree sees it.

One special case is preserved from ContentProcessor, not fixed: the
non-subsection site root is written with a hardcoded weight of 1 and a
different source-URL function (get_root_source_url, not get_source_url),
straight to base_path/_index.md -- exactly mirroring
ContentProcessor._generate_root_file, which never went through the normal
per-heading write path.

A second special case from ContentProcessor.processor.py is deliberately
*not* ported: a heading-text match on 'Interfaces vs. Abstract Classes' that
synthesized a deep-dives/_index.md landing page. Tracing it showed it can
never fire in the real pipeline -- the only heading with that exact text is
always a level-1 sub-section heading, and just above that special case,
ContentProcessor._generate_heading_file forces path_parts to [] for every
level-1 heading, so the special case's `path_parts == ['deep-dives']` guard
can never be true. Confirmed against the real generated
content/clean-code/deep-dives/_index.md, whose source URL matches
main.py's separate, unconditional deep-dives/_index.md write -- not the
URL format the dead special case would have produced.
"""
import os
import tempfile
import unittest

from scripts.tree import Page
from scripts.writer import write_tree


def leaf(title, path_parts, weight, content='Some content.', raw_content=None):
    return Page(
        title=title,
        content=content,
        raw_content=raw_content if raw_content is not None else content,
        path_parts=path_parts,
        level=len(path_parts) + 1,
        line=1,
        weight=weight,
        children=[],
    )


class WriteTreeNonSubsectionTests(unittest.TestCase):
    def test_root_is_written_to_index_at_base_path_with_hardcoded_weight_and_root_source_url(self):
        chapter = leaf("Chapter", ["chapter"], weight=10)
        root = Page(
            title="Site Title", content="Intro.", raw_content="Intro.",
            path_parts=[], level=1, line=1, weight=1, children=[chapter],
        )

        with tempfile.TemporaryDirectory() as tmp:
            write_tree(root, tmp, source_file="/src/CleanABAP.md", is_subsection=False)

            with open(os.path.join(tmp, '_index.md'), encoding='utf-8') as f:
                text = f.read()

        self.assertIn('title: "Site Title"', text)
        self.assertIn('weight: 1', text)
        self.assertIn(
            'source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#L1"',
            text,
        )
        self.assertIn("Intro.", text)

    def test_descendants_written_under_their_path_parts_using_normal_source_url(self):
        chapter = leaf("Chapter", ["chapter"], weight=10)
        root = Page(
            title="Site Title", content="Intro.", raw_content="Intro.",
            path_parts=[], level=1, line=1, weight=1, children=[chapter],
        )

        with tempfile.TemporaryDirectory() as tmp:
            write_tree(root, tmp, source_file="/src/CleanABAP.md", is_subsection=False)

            with open(os.path.join(tmp, 'chapter', 'index.md'), encoding='utf-8') as f:
                text = f.read()

        self.assertIn('title: "Chapter"', text)
        self.assertIn('weight: 10', text)
        self.assertIn('#chapter"', text)

    def test_filename_is_underscore_index_when_page_has_children_else_index(self):
        child = leaf("Child", ["parent", "child"], weight=10)
        parent = leaf("Parent", ["parent"], weight=10)
        parent.children = [child]
        root = Page(
            title="Site Title", content="", raw_content="",
            path_parts=[], level=1, line=1, weight=1, children=[parent],
        )

        with tempfile.TemporaryDirectory() as tmp:
            write_tree(root, tmp, source_file="/src/CleanABAP.md", is_subsection=False)

            self.assertTrue(os.path.isfile(os.path.join(tmp, 'parent', '_index.md')))
            self.assertTrue(os.path.isfile(os.path.join(tmp, 'parent', 'child', 'index.md')))

    def test_returns_count_of_files_written(self):
        chapter = leaf("Chapter", ["chapter"], weight=10)
        root = Page(
            title="Site Title", content="Intro.", raw_content="Intro.",
            path_parts=[], level=1, line=1, weight=1, children=[chapter],
        )

        with tempfile.TemporaryDirectory() as tmp:
            count = write_tree(root, tmp, source_file="/src/CleanABAP.md", is_subsection=False)

        self.assertEqual(count, 2)  # root + chapter

    def test_images_are_not_copied_for_non_subsection_content(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as out_dir:
            source_file = os.path.join(src_dir, "CleanABAP.md")
            with open(source_file, 'w') as f:
                f.write("# Site Title\n")
            with open(os.path.join(src_dir, "pic.png"), 'wb') as f:
                f.write(b'fake-image-bytes')

            chapter = leaf("Chapter", ["chapter"], weight=10, content="![alt](pic.png)")
            chapter.raw_content = "![alt](pic.png)"
            root = Page(
                title="Site Title", content="", raw_content="",
                path_parts=[], level=1, line=1, weight=1, children=[chapter],
            )

            write_tree(root, out_dir, source_file=source_file, is_subsection=False)

            self.assertFalse(os.path.exists(os.path.join(out_dir, 'chapter', 'pic.png')))


class WriteTreeSubSectionTests(unittest.TestCase):
    def test_root_is_written_like_any_other_page_not_specially(self):
        root = Page(
            title="Deep Dive Title", content="Intro.", raw_content="Intro.",
            path_parts=[], level=1, line=1, weight=30, children=[],
        )

        with tempfile.TemporaryDirectory() as tmp:
            write_tree(root, tmp, source_file="/src/sub-sections/DeepDive.md", is_subsection=True)

            with open(os.path.join(tmp, 'index.md'), encoding='utf-8') as f:
                text = f.read()

        self.assertIn('title: "Deep Dive Title"', text)
        self.assertIn('weight: 30', text)  # NOT hardcoded to 1, unlike the site root
        self.assertIn('sub-sections/DeepDive.md#deep-dive-title', text)

    def test_images_referenced_in_raw_content_are_copied_to_the_page_folder(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as out_dir:
            source_file = os.path.join(src_dir, "sub-sections", "DeepDive.md")
            os.makedirs(os.path.dirname(source_file))
            with open(source_file, 'w') as f:
                f.write("# Deep Dive Title\n")
            with open(os.path.join(os.path.dirname(source_file), "pic.png"), 'wb') as f:
                f.write(b'fake-image-bytes')

            chapter = leaf("Chapter", ["chapter"], weight=10, content="![alt](pic.png)")
            root = Page(
                title="Deep Dive Title", content="Intro.", raw_content="Intro.",
                path_parts=[], level=1, line=1, weight=30, children=[chapter],
            )

            write_tree(root, out_dir, source_file=source_file, is_subsection=True)

            self.assertTrue(os.path.isfile(os.path.join(out_dir, 'chapter', 'pic.png')))

    def test_vsdx_files_are_never_copied(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as out_dir:
            source_file = os.path.join(src_dir, "sub-sections", "DeepDive.md")
            os.makedirs(os.path.dirname(source_file))
            with open(source_file, 'w') as f:
                f.write("# Deep Dive Title\n")
            with open(os.path.join(os.path.dirname(source_file), "diagram.vsdx"), 'wb') as f:
                f.write(b'fake-visio-bytes')

            chapter = leaf("Chapter", ["chapter"], weight=10, content="![alt](diagram.vsdx)")
            root = Page(
                title="Deep Dive Title", content="Intro.", raw_content="Intro.",
                path_parts=[], level=1, line=1, weight=30, children=[chapter],
            )

            write_tree(root, out_dir, source_file=source_file, is_subsection=True)

            self.assertFalse(os.path.isfile(os.path.join(out_dir, 'chapter', 'diagram.vsdx')))


if __name__ == '__main__':
    unittest.main()
