"""
Tests for scripts/utils.py's load_link_titles.
"""
import os
import tempfile
import unittest

from scripts.utils import load_link_titles


class LoadLinkTitlesTests(unittest.TestCase):
    def test_returns_empty_dict_when_mapping_file_does_not_exist(self):
        with tempfile.TemporaryDirectory() as repo_root:
            self.assertEqual(load_link_titles(repo_root), {})

    def test_reads_the_linktitles_table_from_data_mapping_toml(self):
        with tempfile.TemporaryDirectory() as repo_root:
            data_dir = os.path.join(repo_root, 'data')
            os.makedirs(data_dir)
            with open(os.path.join(data_dir, 'mapping.toml'), 'w', encoding='utf-8') as f:
                f.write('[linktitles]\n"how-to/how-to-get-started" = "Get Started"\n')

            self.assertEqual(
                load_link_titles(repo_root),
                {"how-to/how-to-get-started": "Get Started"},
            )


if __name__ == '__main__':
    unittest.main()
