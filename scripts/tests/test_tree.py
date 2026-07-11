"""
Tests for scripts/tree.py, written test-first against the interface designed
during the candidate #2 architecture-review grilling session.

tree.py replaces scripts/processor.py's ContentProcessor with three pure
"markdown text in, page tree out" stages (parse_tree, resolve_links,
apply_text_fixups) plus a Page dataclass. Two subtleties from processor.py
are deliberately reproduced here, not fixed:

1. KNOWN BUG -- weight is only correctly position-based for the top two
   heading levels. ContentProcessor._calculate_weight looked up a heading's
   siblings by scanning only a shallow, non-recursively-nested `structure`
   list; anything past that lookup's reach silently fell back to a constant
   weight. Traced against real content and confirmed in the actual generated
   site (see architecture-review handoff): three '####'-level siblings under
   classes/classes-object-orientation/ all get weight 10, and three '##'
   -level siblings inside the Enumerations deep-dive all get weight 20
   (identical to their own parent's weight). Fixing this would change
   content/ output, so it's preserved exactly:
     - main content: level 2 and level 3 headings get correct 1-based
       sibling-position * 10 weight; level 4+ always get weight 10.
     - sub-sections: level 1 (root) and level 2 headings all get the same
       base_weight = (subsection_index + 1) * 10; level 3+ always get 10.
2. The root page's content pipeline is asymmetric: ContentProcessor.
   _generate_root_file (used only for the non-subsection site root) never
   called _fix_image_references/_fix_below_references, only cross-reference
   conversion -- unlike every other page, which got both. apply_text_fixups
   reproduces this by skipping the top node when is_subsection is False.

has_children is NOT bug-for-bug ported from _has_children's convoluted
two-path lookup: tracing it showed its fallback path (a prefix-match scan
over the flat all_headings list) already computes "does this heading have
any descendant at any depth", which is exactly what `len(page.children) > 0`
gives for free on a tree that nests every heading level correctly (unlike
`structure`, parse_tree's tree does nest every level, since it drives what
actually gets written -- see the level 4/5 headings test below).
"""
import unittest

from scripts.tree import Page, apply_text_fixups, parse_tree, resolve_links, walk
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

    def test_known_bug_level_4_siblings_all_get_weight_10(self):
        # Both are children of "First Chapter Sub A"; a correct sibling
        # position would give 10 and 20, but the old algorithm's shallow
        # sibling lookup never reaches this deep, so both fall back to 10.
        self.assertEqual(find(self.root, "Deeply Nested One").weight, 10)
        self.assertEqual(find(self.root, "Deeply Nested Two").weight, 10)

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

    def test_known_bug_level_2_siblings_all_get_the_root_base_weight(self):
        # Not position-based: every level-2 heading in a sub-section shares
        # the parent's base_weight, indistinguishable from each other.
        self.assertEqual(find(self.root, "Section One").weight, 30)
        self.assertEqual(find(self.root, "Section Two").weight, 30)

    def test_known_bug_level_3_heading_gets_constant_weight_10(self):
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


if __name__ == '__main__':
    unittest.main()
