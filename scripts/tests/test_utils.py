"""
Tests for scripts/utils.py's MappingConfig.
"""
import os
import tempfile
import unittest

from scripts.utils import MappingConfig, remove_breadcrumb_lines


def write_mapping_toml(repo_root, text):
    data_dir = os.path.join(repo_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, 'mapping.toml'), 'w', encoding='utf-8') as f:
        f.write(text)


def load_with_files_table(repo_root, text):
    # Every case below needs a valid [files] table (MappingConfig.load
    # requires one) alongside whatever it's actually testing.
    write_mapping_toml(repo_root, '[files]\nchapterize = ["CleanABAP.md"]\nkeep = []\n\n' + text)
    return MappingConfig.load(repo_root)


class MappingConfigPreserveTests(unittest.TestCase):
    def test_empty_when_content_preserve_is_absent(self):
        with tempfile.TemporaryDirectory() as repo_root:
            config = load_with_files_table(repo_root, '')
            self.assertEqual(config.preserve, set())

    def test_reads_the_content_preserve_list(self):
        with tempfile.TemporaryDirectory() as repo_root:
            config = load_with_files_table(repo_root, '[content]\npreserve = ["legal.md"]\n')
            self.assertEqual(config.preserve, {'legal.md'})


class MappingConfigLinkTitlesTests(unittest.TestCase):
    def test_empty_when_linktitles_is_absent(self):
        with tempfile.TemporaryDirectory() as repo_root:
            config = load_with_files_table(repo_root, '')
            self.assertEqual(config.link_titles, {})

    def test_reads_the_linktitles_table(self):
        with tempfile.TemporaryDirectory() as repo_root:
            config = load_with_files_table(
                repo_root, '[linktitles]\n"how-to/how-to-get-started" = "Get Started"\n',
            )
            self.assertEqual(config.link_titles, {"how-to/how-to-get-started": "Get Started"})


class MappingConfigDiagramsTests(unittest.TestCase):
    def test_empty_when_diagrams_is_absent(self):
        with tempfile.TemporaryDirectory() as repo_root:
            config = load_with_files_table(repo_root, '')
            self.assertEqual(config.diagrams, {})

    def test_reads_the_diagrams_table(self):
        with tempfile.TemporaryDirectory() as repo_root:
            config = load_with_files_table(
                repo_root,
                "[diagrams]\n"
                '"Foo.png" = \'\'\'\n'
                "```mermaid\n"
                "classDiagram\n"
                "    A --> B\n"
                "```\'\'\'\n",
            )
            self.assertEqual(config.diagrams, {"Foo.png": "```mermaid\nclassDiagram\n    A --> B\n```"})


class MappingConfigFilesTests(unittest.TestCase):
    def test_reads_chapterize_and_keep_lists(self):
        with tempfile.TemporaryDirectory() as repo_root:
            write_mapping_toml(
                repo_root,
                '[files]\n'
                'chapterize = ["CleanABAP.md", "sub-sections/ModernABAPLanguageElements.md"]\n'
                'keep = ["sub-sections/AvoidEncodings.md"]\n',
            )

            config = MappingConfig.load(repo_root)

            self.assertEqual(
                config.files,
                {
                    'chapterize': ["CleanABAP.md", "sub-sections/ModernABAPLanguageElements.md"],
                    'keep': ["sub-sections/AvoidEncodings.md"],
                },
            )

    def test_raises_when_mapping_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as repo_root:
            with self.assertRaises(ValueError):
                MappingConfig.load(repo_root)

    def test_raises_when_files_table_is_missing(self):
        with tempfile.TemporaryDirectory() as repo_root:
            write_mapping_toml(repo_root, '[linktitles]\n"chapter" = "Chapter"\n')

            with self.assertRaises(ValueError):
                MappingConfig.load(repo_root)


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
