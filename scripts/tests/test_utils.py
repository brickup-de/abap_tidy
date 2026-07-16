"""
Tests for scripts/utils.py's load_link_titles and load_file_config.
"""
import os
import tempfile
import unittest

from scripts.utils import load_file_config, load_link_titles, remove_breadcrumb_lines


def write_mapping_toml(repo_root, text):
    data_dir = os.path.join(repo_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, 'mapping.toml'), 'w', encoding='utf-8') as f:
        f.write(text)


class LoadLinkTitlesTests(unittest.TestCase):
    def test_returns_empty_dict_when_mapping_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as repo_root:
            self.assertEqual(load_link_titles(repo_root), {})

    def test_reads_the_linktitles_table_from_data_mapping_toml(self):
        with tempfile.TemporaryDirectory() as repo_root:
            write_mapping_toml(repo_root, '[linktitles]\n"how-to/how-to-get-started" = "Get Started"\n')

            self.assertEqual(
                load_link_titles(repo_root),
                {"how-to/how-to-get-started": "Get Started"},
            )


class LoadFileConfigTests(unittest.TestCase):
    def test_reads_chapterize_and_keep_lists_from_data_mapping_toml(self):
        with tempfile.TemporaryDirectory() as repo_root:
            write_mapping_toml(
                repo_root,
                '[files]\n'
                'chapterize = ["CleanABAP.md", "sub-sections/ModernABAPLanguageElements.md"]\n'
                'keep = ["sub-sections/AvoidEncodings.md"]\n',
            )

            self.assertEqual(
                load_file_config(repo_root),
                {
                    'chapterize': ["CleanABAP.md", "sub-sections/ModernABAPLanguageElements.md"],
                    'keep': ["sub-sections/AvoidEncodings.md"],
                },
            )

    def test_raises_when_mapping_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as repo_root:
            with self.assertRaises(ValueError):
                load_file_config(repo_root)

    def test_raises_when_files_table_is_missing(self):
        with tempfile.TemporaryDirectory() as repo_root:
            write_mapping_toml(repo_root, '[linktitles]\n"chapter" = "Chapter"\n')

            with self.assertRaises(ValueError):
                load_file_config(repo_root)


class RemoveBreadcrumbLinesTests(unittest.TestCase):
    def test_removes_root_guide_breadcrumb(self):
        lines = [
            '> [Clean ABAP](#clean-abap) > [Content](#content) > [This section](#how-to)',
            'Some text.',
        ]

        self.assertEqual(remove_breadcrumb_lines(lines), ['Some text.'])

    def test_removes_sub_section_breadcrumb_not_starting_with_clean_abap(self):
        # Enumerations.md's internal nav starts with the section's own
        # name, not "Clean ABAP" -- it must be stripped too.
        lines = [
            '> [Enumerations](#enumerations) > [This section](#native-enumerations)',
            'Some text.',
        ]

        self.assertEqual(remove_breadcrumb_lines(lines), ['Some text.'])

    def test_keeps_ordinary_blockquotes_that_are_not_breadcrumbs(self):
        lines = [
            '> Note that the [`STRUCTURE` addition](https://example.com) is not used.',
        ]

        self.assertEqual(remove_breadcrumb_lines(lines), lines)


if __name__ == '__main__':
    unittest.main()
