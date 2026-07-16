"""
Tests for scripts/tree.py, written test-first against the interface designed
during the candidate #2 architecture-review grilling session.

tree.py replaces scripts/processor.py's ContentProcessor with three pure
"markdown text in, page tree out" stages (parse_tree, resolve_links,
apply_text_fixups) plus a Page dataclass.

One subtlety from processor.py is deliberately reproduced here, not fixed:
the root page's content pipeline is asymmetric. ContentProcessor.
_generate_root_file (used only for the non-subsection site root) never
called _fix_image_references/_fix_below_references, only cross-reference
conversion -- unlike every other page, which got both. apply_text_fixups
reproduces this by skipping the top node when is_subsection is False.

One bug from processor.py is deliberately NOT reproduced: weight there was
only correctly position-based for the top two heading levels.
ContentProcessor._calculate_weight looked up a heading's siblings by
scanning only a shallow, non-recursively-nested `structure` list; anything
past that lookup's reach silently fell back to a constant weight. Traced
against real content and confirmed in the actual rendered site: Hugo's
sidebar tie-breaks equal weights alphabetically, so three '####'-level
siblings under classes/classes-object-orientation/ (all weight 10 under the
old code) rendered in alphabetical order instead of the guide's intended
reading order, and the same for the Enumerations deep-dive's top-level
sections (all weight 20 under the old code). Fixed here by weighting every
non-root page by its true 1-based position among its actual parent's
children, at every depth -- trivial since parse_tree's tree nests every
heading level correctly to begin with (see the has_children note below).

has_children is NOT bug-for-bug ported from _has_children's convoluted
two-path lookup: tracing it showed its fallback path (a prefix-match scan
over the flat all_headings list) already computes "does this heading have
any descendant at any depth", which is exactly what `len(page.children) > 0`
gives for free on a tree that nests every heading level correctly (unlike
`structure`, parse_tree's tree does nest every level, since it drives what
actually gets written -- see the level 4/5 headings test below).
"""
import unittest

from scripts.tree import Page, apply_text_fixups, flatten_to_single_page, parse_tree, resolve_links, walk
from scripts.crossref import CrossReferenceConverter


def find(root: Page, title: str) -> Page:
    for page in walk(root):
        if page.title == title:
            return page
    raise AssertionError(f"no page titled {title!r} in tree")


MAIN_CONTENT = """\
# Site Title

Intro paragraph.

## First Chapter

First chapter content.

### First Chapter Sub A

Sub A content.

#### Deeply Nested One

Deep content one.

#### Deeply Nested Two

Deep content two.

### First Chapter Sub B

Sub B content.

## Second Chapter

Second chapter content.
"""


class ParseTreeMainContentTests(unittest.TestCase):
    def setUp(self):
        self.root = parse_tree(MAIN_CONTENT, is_subsection=False)

    def test_root_is_the_level_1_heading(self):
        self.assertEqual(self.root.title, "Site Title")
        self.assertEqual(self.root.content, "Intro paragraph.")
        self.assertEqual(self.root.path_parts, [])
        self.assertEqual(self.root.level, 1)
        self.assertEqual(self.root.weight, 1)

    def test_level_2_siblings_get_correct_sequential_weight(self):
        self.assertEqual(find(self.root, "First Chapter").weight, 10)
        self.assertEqual(find(self.root, "Second Chapter").weight, 20)

    def test_level_3_siblings_get_correct_sequential_weight_per_parent(self):
        self.assertEqual(find(self.root, "First Chapter Sub A").weight, 10)
        self.assertEqual(find(self.root, "First Chapter Sub B").weight, 20)

    def test_level_4_siblings_get_correct_sequential_weight_per_parent(self):
        # Both are children of "First Chapter Sub A". Unlike the old
        # ContentProcessor, whose shallow sibling lookup never reached this
        # deep and fell back to a constant weight 10 for both, parse_tree
        # weights every depth by true position among its actual parent.
        self.assertEqual(find(self.root, "Deeply Nested One").weight, 10)
        self.assertEqual(find(self.root, "Deeply Nested Two").weight, 20)

    def test_path_parts_nest_correctly_at_every_depth(self):
        self.assertEqual(find(self.root, "First Chapter").path_parts, ["first-chapter"])
        self.assertEqual(
            find(self.root, "First Chapter Sub A").path_parts,
            ["first-chapter", "first-chapter-sub-a"],
        )
        self.assertEqual(
            find(self.root, "Deeply Nested One").path_parts,
            ["first-chapter", "first-chapter-sub-a", "deeply-nested-one"],
        )

    def test_has_children_reflects_real_nesting_at_every_depth(self):
        self.assertTrue(self.root.has_children)
        self.assertTrue(find(self.root, "First Chapter").has_children)
        self.assertTrue(find(self.root, "First Chapter Sub A").has_children)
        self.assertFalse(find(self.root, "First Chapter Sub B").has_children)
        self.assertFalse(find(self.root, "Second Chapter").has_children)
        self.assertFalse(find(self.root, "Deeply Nested One").has_children)
        self.assertFalse(find(self.root, "Deeply Nested Two").has_children)

    def test_content_is_captured_and_stripped(self):
        self.assertEqual(find(self.root, "First Chapter").content, "First chapter content.")
        self.assertEqual(find(self.root, "Second Chapter").content, "Second chapter content.")

    def test_tree_actually_nests_level_4_headings_for_traversal(self):
        # Unlike ContentProcessor.structure (which orphans level 4+ headings
        # from its nested tree, relying on a separate flat all_headings list
        # for file generation), parse_tree's tree must nest every level so a
        # tree-walking writer can reach and write them.
        sub_a = find(self.root, "First Chapter Sub A")
        self.assertEqual(
            {c.title for c in sub_a.children},
            {"Deeply Nested One", "Deeply Nested Two"},
        )


class ParseTreeContentBoundaryTests(unittest.TestCase):
    def test_content_before_first_heading_is_dropped(self):
        text = "Stray preamble line.\n\n# Title\n\nBody.\n"
        root = parse_tree(text, is_subsection=False)
        self.assertEqual(root.content, "Body.")

    def test_trailing_content_after_last_heading_is_captured(self):
        text = "# Title\n\n## Only Chapter\n\nTrailing body text.\n"
        root = parse_tree(text, is_subsection=False)
        self.assertEqual(find(root, "Only Chapter").content, "Trailing body text.")

    def test_base_line_offsets_reported_line_numbers(self):
        text = "# Title\n\n## Chapter\n\nBody.\n"
        root = parse_tree(text, is_subsection=False, base_line=100)
        chapter = find(root, "Chapter")
        self.assertGreater(chapter.line, 100)


SUBSECTION_CONTENT = """\
# Deep Dive Title

Deep dive intro.

## Section One

Section one content.

## Section Two

Section two content.

### Section Two Sub

Sub content.
"""


class ParseTreeSubSectionTests(unittest.TestCase):
    def setUp(self):
        self.root = parse_tree(SUBSECTION_CONTENT, is_subsection=True, subsection_index=2)

    def test_root_weight_is_base_weight(self):
        # base_weight = (subsection_index + 1) * 10 = (2 + 1) * 10
        self.assertEqual(self.root.weight, 30)
        self.assertEqual(self.root.path_parts, [])

    def test_level_2_siblings_get_correct_sequential_weight(self):
        # Position-based among the root's own children, not the old
        # ContentProcessor's constant base_weight shared by every sibling.
        self.assertEqual(find(self.root, "Section One").weight, 10)
        self.assertEqual(find(self.root, "Section Two").weight, 20)

    def test_level_3_heading_gets_correct_position_based_weight(self):
        self.assertEqual(find(self.root, "Section Two Sub").weight, 10)

    def test_has_children(self):
        self.assertFalse(find(self.root, "Section One").has_children)
        self.assertTrue(find(self.root, "Section Two").has_children)
        self.assertFalse(find(self.root, "Section Two Sub").has_children)

    def test_path_parts_exclude_the_root_heading_folder(self):
        self.assertEqual(find(self.root, "Section One").path_parts, ["section-one"])
        self.assertEqual(
            find(self.root, "Section Two Sub").path_parts,
            ["section-two", "section-two-sub"],
        )


class ResolveLinksTests(unittest.TestCase):
    def test_converts_content_at_every_depth_including_root(self):
        text = (
            "# Title\n\nSee [a link](#some-target).\n\n"
            "## Chapter\n\nAlso see [a link](#some-target).\n"
        )
        root = parse_tree(text, is_subsection=False)
        converter = CrossReferenceConverter({"some-target": "/clean-code/some-target/"})

        resolved = resolve_links(root, converter)

        self.assertEqual(resolved.content, "See [a link](/clean-code/some-target/).")
        self.assertEqual(
            find(resolved, "Chapter").content,
            "Also see [a link](/clean-code/some-target/).",
        )

    def test_does_not_mutate_the_input_tree(self):
        text = "# Title\n\nSee [a link](#some-target).\n"
        root = parse_tree(text, is_subsection=False)
        original_content = root.content
        converter = CrossReferenceConverter({"some-target": "/clean-code/some-target/"})

        resolve_links(root, converter)

        self.assertEqual(root.content, original_content)


class FlattenToSinglePageTests(unittest.TestCase):
    def test_reconstructs_headings_and_content_in_document_order(self):
        root = parse_tree(SUBSECTION_CONTENT, is_subsection=True, subsection_index=2)

        flattened = flatten_to_single_page(root)

        self.assertEqual(
            flattened.content,
            "Deep dive intro.\n\n"
            "## Section One\n\nSection one content.\n\n"
            "## Section Two\n\nSection two content.\n\n"
            "### Section Two Sub\n\nSub content."
        )

    def test_result_is_a_leaf_preserving_root_identity_fields(self):
        root = parse_tree(SUBSECTION_CONTENT, is_subsection=True, subsection_index=2)

        flattened = flatten_to_single_page(root)

        self.assertEqual(flattened.children, [])
        self.assertEqual(flattened.title, "Deep Dive Title")
        self.assertEqual(flattened.level, 1)
        self.assertEqual(flattened.weight, root.weight)

    def test_flattens_content_and_raw_content_independently(self):
        # apply_text_fixups only ever rewrites .content, leaving .raw_content
        # as the original source text (see writer.py's _copy_images_for_content,
        # which needs the original relative image path to find the file on
        # disk). Flattening must keep that same split for the combined page.
        child = Page(
            title="Child", content="CHILD_FIXED", raw_content="CHILD_RAW",
            path_parts=["child"], level=2, line=5, weight=10, children=[],
        )
        root = Page(
            title="Root", content="ROOT_FIXED", raw_content="ROOT_RAW",
            path_parts=[], level=1, line=1, weight=10, children=[child],
        )

        flattened = flatten_to_single_page(root)

        self.assertEqual(flattened.content, "ROOT_FIXED\n\n## Child\n\nCHILD_FIXED")
        self.assertEqual(flattened.raw_content, "ROOT_RAW\n\n## Child\n\nCHILD_RAW")

    def test_does_not_mutate_the_input_tree(self):
        root = parse_tree(SUBSECTION_CONTENT, is_subsection=True, subsection_index=0)
        original_children_count = len(root.children)

        flatten_to_single_page(root)

        self.assertEqual(len(root.children), original_children_count)
        self.assertNotEqual(root.content, "Deep dive intro.\n\n## Section One\n\nSection one content.")


class ApplyTextFixupsTests(unittest.TestCase):
    def test_fixes_image_paths_to_bare_filename(self):
        text = "# Title\n\n## Chapter\n\n![alt](some/deep/path/pic.png)\n"
        root = parse_tree(text, is_subsection=False)

        fixed = apply_text_fixups(root, is_subsection=False)

        self.assertEqual(find(fixed, "Chapter").content, "![alt](pic.png)")

    def test_fixes_below_references(self):
        text = "# Title\n\n## Chapter\n\nSee the rules below for details.\n"
        root = parse_tree(text, is_subsection=False)

        fixed = apply_text_fixups(root, is_subsection=False)

        self.assertEqual(find(fixed, "Chapter").content, "See the related rules for details.")

    def test_non_subsection_root_is_exempt_from_fixups(self):
        # Matches ContentProcessor._generate_root_file, which only ever
        # applied cross-reference conversion to the site root's content --
        # never _fix_image_references or _fix_below_references.
        text = "# Title\n\n![alt](some/deep/path/pic.png)\n\n## Chapter\n\nBody.\n"
        root = parse_tree(text, is_subsection=False)

        fixed = apply_text_fixups(root, is_subsection=False)

        self.assertEqual(fixed.content, "![alt](some/deep/path/pic.png)")

    def test_subsection_root_does_get_fixups(self):
        # Unlike the site root, a sub-section's root heading is written via
        # the normal per-heading path in ContentProcessor, so it does get
        # both fixups applied.
        text = "# Title\n\n![alt](some/deep/path/pic.png)\n"
        root = parse_tree(text, is_subsection=True, subsection_index=0)

        fixed = apply_text_fixups(root, is_subsection=True)

        self.assertEqual(fixed.content, "![alt](pic.png)")

    def test_does_not_mutate_the_input_tree(self):
        text = "# Title\n\n## Chapter\n\n![alt](some/deep/path/pic.png)\n"
        root = parse_tree(text, is_subsection=False)
        original = find(root, "Chapter").content

        apply_text_fixups(root, is_subsection=False)

        self.assertEqual(find(root, "Chapter").content, original)

    def test_image_matching_a_diagrams_override_is_replaced_with_the_stored_block(self):
        text = "# Title\n\n## Chapter\n\n![](Foo.png)\n"
        root = parse_tree(text, is_subsection=False)
        diagrams = {"Foo.png": "```mermaid\nclassDiagram\n    A --> B\n```"}

        fixed = apply_text_fixups(root, is_subsection=False, diagrams=diagrams)

        self.assertEqual(find(fixed, "Chapter").content, "```mermaid\nclassDiagram\n    A --> B\n```")

    def test_diagram_override_matches_by_basename_ignoring_subdirectory_prefix(self):
        # Real source images live alongside their sub-section file under a
        # subdirectory, e.g. interfaces-vs-abstract-classes/Foo.png -- the
        # [diagrams] table is keyed by bare basename (see data/mapping.toml),
        # matching how _fix_image_references already normalizes paths.
        text = "# Title\n\n## Chapter\n\n![](interfaces-vs-abstract-classes/Foo.png)\n"
        root = parse_tree(text, is_subsection=False)
        diagrams = {"Foo.png": "```mermaid\nclassDiagram\n    A --> B\n```"}

        fixed = apply_text_fixups(root, is_subsection=False, diagrams=diagrams)

        self.assertEqual(find(fixed, "Chapter").content, "```mermaid\nclassDiagram\n    A --> B\n```")

    def test_diagram_override_also_replaces_raw_content(self):
        # raw_content must lose the image reference too, or writer.py's
        # _copy_images_for_content (which scans raw_content, not content)
        # would still copy the now-orphaned PNG into the output folder.
        text = "# Title\n\n## Chapter\n\n![](Foo.png)\n"
        root = parse_tree(text, is_subsection=False)
        diagrams = {"Foo.png": "```mermaid\nclassDiagram\n    A --> B\n```"}

        fixed = apply_text_fixups(root, is_subsection=False, diagrams=diagrams)

        self.assertEqual(find(fixed, "Chapter").raw_content, "```mermaid\nclassDiagram\n    A --> B\n```")

    def test_image_without_a_diagram_override_is_unaffected_by_the_diagrams_param(self):
        text = "# Title\n\n## Chapter\n\n![alt](some/deep/path/pic.png)\n"
        root = parse_tree(text, is_subsection=False)
        diagrams = {"Foo.png": "```mermaid\nclassDiagram\n    A --> B\n```"}

        fixed = apply_text_fixups(root, is_subsection=False, diagrams=diagrams)

        self.assertEqual(find(fixed, "Chapter").content, "![alt](pic.png)")
        self.assertEqual(find(fixed, "Chapter").raw_content, "![alt](some/deep/path/pic.png)")

    def test_diagrams_defaults_to_no_overrides_when_omitted(self):
        text = "# Title\n\n## Chapter\n\n![](Foo.png)\n"
        root = parse_tree(text, is_subsection=False)

        fixed = apply_text_fixups(root, is_subsection=False)

        self.assertEqual(find(fixed, "Chapter").content, "![](Foo.png)")

    def test_fixes_shorthand_longhand_table(self):
        text = (
            "# Title\n\n## Chapter\n\n"
            "Shorthand | Longhand  |\n"
            "---|---|\n"
            "x += 1.  | x = x + 1.  |\n"
            "x &&= \\`abc\\`. | x = x && \\`abc\\`. |\n"
        )
        root = parse_tree(text, is_subsection=False)

        fixed = apply_text_fixups(root, is_subsection=False)

        self.assertEqual(
            find(fixed, "Chapter").content,
            "```ABAP\n"
            "x += 1. \" short\n"
            "x = x + 1. \" long\n"
            "\n"
            "x &&= `abc`. \" short\n"
            "x = x && `abc`. \" long\n"
            "```"
        )


if __name__ == '__main__':
    unittest.main()
