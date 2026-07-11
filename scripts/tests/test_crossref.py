"""
Characterization tests for scripts/crossref.py.

These pin down CrossReferenceConverter's and build_path_mapping's current
behavior branch by branch, including two convert_link branches that a trace
against the real Clean ABAP content never actually reached (0 hits each --
see the architecture review that led to this file), and a known-buggy
fallback. None of that behavior is changed here: this is "characterize
first," not "fix first." Deleting dead branches and fixing the fallback's
guessed paths are deliberately left as follow-up work.
"""
import unittest

from scripts.crossref import CrossReferenceConverter, build_path_mapping


class BuildPathMappingTests(unittest.TestCase):
    def test_emits_lowercase_text_kebab_and_hash_kebab_keys(self):
        headings = [{
            'text': 'Use Descriptive Names',
            'path': '/clean-code/names/use-descriptive-names/',
            'level': 3,
        }]
        mapping = build_path_mapping(headings)

        self.assertEqual(mapping['use descriptive names'], '/clean-code/names/use-descriptive-names/')
        self.assertEqual(mapping['use-descriptive-names'], '/clean-code/names/use-descriptive-names/')
        self.assertEqual(mapping['#use-descriptive-names'], '/clean-code/names/use-descriptive-names/')

    def test_kebab_lower_key_is_a_redundant_duplicate_of_the_kebab_key(self):
        # kebab_text = github_anchor(text) is already lowercase, so
        # `mapping[kebab_text.lower()] = path` writes the same key as
        # `mapping[kebab_text] = path` just above it. Only 3 distinct keys
        # survive from the 4 assignments build_path_mapping makes per
        # heading. Documented here as current behavior, not simplified.
        headings = [{'text': 'Some Heading', 'path': '/p/', 'level': 2}]
        mapping = build_path_mapping(headings)

        self.assertEqual(set(mapping.keys()), {'some heading', 'some-heading', '#some-heading'})
        self.assertEqual(len(mapping), 3)

    def test_accumulates_keys_across_multiple_headings(self):
        headings = [
            {'text': 'First', 'path': '/p1/', 'level': 2},
            {'text': 'Second', 'path': '/p2/', 'level': 2},
        ]
        mapping = build_path_mapping(headings)

        self.assertEqual(mapping['first'], '/p1/')
        self.assertEqual(mapping['second'], '/p2/')


class PassthroughTests(unittest.TestCase):
    def test_absolute_path_is_left_unchanged(self):
        converter = CrossReferenceConverter({})
        self.assertEqual(
            converter.convert_link('text', '/already/absolute/'),
            '[text](/already/absolute/)',
        )

    def test_http_url_is_left_unchanged(self):
        converter = CrossReferenceConverter({})
        self.assertEqual(
            converter.convert_link('text', 'https://example.com'),
            '[text](https://example.com)',
        )


class FileLinkPatternTests(unittest.TestCase):
    """The 6 distinguishable outputs FILE_LINK_PATTERN's special-casing can produce."""

    def setUp(self):
        # Shared mapping used by the two fragment cases, which fall through
        # to ordinary anchor resolution after stripping the file prefix.
        self.converter = CrossReferenceConverter({
            'some-anchor': '/clean-code/some-anchor/',
        })

    def test_file_link_cases(self):
        cases = [
            ('main guide, no fragment', 'CleanABAP.md', '[text](/clean-code/)'),
            ('main guide, with fragment', 'CleanABAP.md#some-anchor', '[text](/clean-code/some-anchor/)'),
            ('sub-section, no fragment', 'sub-sections/Enumerations.md', '[text](/clean-code/deep-dives/enumerations/)'),
            ('sub-section, with fragment', 'sub-sections/Enumerations.md#some-anchor', '[text](/clean-code/some-anchor/)'),
            ('external, with up_dir', '../CONTRIBUTING.md', '[text](https://github.com/SAP/styleguides/blob/main/CONTRIBUTING.md)'),
            ('external, without up_dir', 'CONTRIBUTING.md', '[text](https://github.com/SAP/styleguides/blob/main/clean-abap/CONTRIBUTING.md)'),
        ]
        for name, anchor, expected in cases:
            with self.subTest(name):
                self.assertEqual(self.converter.convert_link('text', anchor), expected)


class AnchorResolutionOrderTests(unittest.TestCase):
    """The fallback cascade convert_link runs through once no FILE_LINK_PATTERN applies."""

    def test_exact_match_with_hash_prefix(self):
        converter = CrossReferenceConverter({'exact-match': '/clean-code/exact-match/'})
        self.assertEqual(
            converter.convert_link('text', '#exact-match'),
            '[text](/clean-code/exact-match/)',
        )

    def test_exact_match_without_hash_prefix(self):
        converter = CrossReferenceConverter({'some-plain-word': '/clean-code/some-plain-word/'})
        self.assertEqual(
            converter.convert_link('text', 'some-plain-word'),
            '[text](/clean-code/some-plain-word/)',
        )

    def test_kebab_anchor_match_when_raw_anchor_is_not_a_key(self):
        # In the real pipeline this branch is dead: build_path_mapping always
        # stores the github_anchor-normalized form as its own key, so the
        # exact-match check above already catches it (a trace against the
        # real Clean ABAP content showed 0 hits here). Characterized in
        # isolation by handing convert_link a mapping that only has the
        # normalized key, not the raw one.
        converter = CrossReferenceConverter({'some-anchor': '/clean-code/some-anchor/'})
        self.assertEqual(
            converter.convert_link('text', '#Some Anchor'),
            '[text](/clean-code/some-anchor/)',
        )

    def test_closest_match_loop_when_mapping_lacks_a_normalized_key(self):
        # Also dead in the real pipeline for the same reason as above --
        # build_path_mapping stores both the raw-text key and the kebab key
        # for every heading, so the kebab-match check always wins first.
        # Reachable only when path_mapping was built by something other than
        # build_path_mapping. Characterized here directly against
        # convert_link, not through the real mapping builder.
        converter = CrossReferenceConverter({'weird anchor': '/clean-code/weird-anchor/'})
        self.assertEqual(
            converter.convert_link('text', '#weird-anchor'),
            '[text](/clean-code/weird-anchor/)',
        )

    def test_prefix_fallback_appends_remaining_segments(self):
        converter = CrossReferenceConverter({'parent-topic': '/clean-code/parent-topic/'})
        self.assertEqual(
            converter.convert_link('text', '#parent-topic-extra-words'),
            '[text](/clean-code/parent-topic/extra-words/)',
        )

    def test_prefix_fallback_with_no_remaining_segment(self):
        # A trailing hyphen in the normalized anchor produces an empty final
        # path_part, so the matched prefix leaves nothing to append -- the
        # `else: return base_path` line, otherwise unreached by any of the
        # cases above.
        converter = CrossReferenceConverter({'topic': '/clean-code/topic/'})
        self.assertEqual(
            converter.convert_link('text', '#Topic-'),
            '[text](/clean-code/topic/)',
        )

    def test_unresolved_anchor_falls_back_to_a_guessed_path(self):
        converter = CrossReferenceConverter({})
        self.assertEqual(
            converter.convert_link('text', '#totally-unknown-thing'),
            '[text](/clean-code/totally-unknown-thing/)',
        )

    def test_known_bug_unrecognized_file_prefix_produces_a_broken_guess(self):
        # KNOWN BUG, preserved as-is (characterize-first, not fixed here):
        # FILE_LINK_PATTERN only recognizes a "../" or "sub-sections/"
        # prefix before a .md filename. A link into any other directory
        # (e.g. real Clean ABAP content's
        # "[Cheat Sheet](cheat-sheet/CheatSheet.md)") skips the file-link
        # special-casing entirely, and the generic fallback strips the
        # slash and dot without a separator, guessing a folder that was
        # never generated.
        converter = CrossReferenceConverter({})
        self.assertEqual(
            converter.convert_link('text', 'cheat-sheet/CheatSheet.md'),
            '[text](/clean-code/cheat-sheetcheatsheetmd/)',
        )


class ConvertContentTests(unittest.TestCase):
    def test_delegates_each_markdown_link_to_convert_link(self):
        converter = CrossReferenceConverter({'exact-match': '/clean-code/exact-match/'})
        content = "See [the doc](#exact-match) and [absolute](/already/there/)."

        result = converter.convert_content(content)

        self.assertEqual(
            result,
            "See [the doc](/clean-code/exact-match/) and [absolute](/already/there/).",
        )


if __name__ == '__main__':
    unittest.main()
