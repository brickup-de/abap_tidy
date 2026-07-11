"""
Tests for the cross-file cross-reference resolution order fix in
scripts/main.py, written test-first during the grilling session that
confirmed a global two-pass restructure: parse every source file first,
build one complete heading_data set, then resolve+write every tree.

Before this fix, process_clean_abap() resolved the main file against only
its own headings (before any sub-section had been parsed at all), and
process_sub_sections() rebuilt a cumulative mapping per file in
sorted-filename order -- so a link could only ever resolve against files
processed earlier. A link in CleanABAP.md to a sub-section-only heading, or
a link in an alphabetically-early sub-section to an alphabetically-later
one, could never resolve and fell through to CrossReferenceConverter's
guessed-path fallback.

A second, easy-to-miss risk surfaced while designing the fix: naively
flattening every file's headings into one global dict (last-wins on
collision) would let a same-titled heading in a *later-processed* file
silently hijack a same-file self-reference in an *earlier-processed* one.
Three such collisions actually exist in the real source data (heading text
"Exceptions", "Conditions", "Constructors" each appear both in CleanABAP.md
and in a sub-section) -- and CleanABAP.md has real bare `(#anchor)`
self-references to exactly those headings (breadcrumbs, TOC). Before this
fix, main was always resolved against a main-only mapping, so those
self-references always resolved correctly by construction; a naive global
mapping would have silently broken them. The fix resolves each file against
the full global heading set with that file's *own* heading_data appended
last, so its own entries always win ties for itself -- see
RunConversionCrossReferenceOrderTests.test_main_self_reference_is_not_hijacked_...
"""
import os
import tempfile
import unittest

from scripts.main import parse_main, parse_sub_sections, run_conversion


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


class ParseMainTests(unittest.TestCase):
    def test_returns_tree_and_heading_data_excluding_the_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            main_file = os.path.join(tmp, "CleanABAP.md")
            write_file(main_file, "# Clean ABAP\n\nIntro.\n\n## Names\n\nUse descriptive names.\n")

            tree, heading_data = parse_main(main_file)

        self.assertEqual(tree.title, "Clean ABAP")
        self.assertEqual(heading_data, [
            {'text': 'Names', 'path': '/clean-code/names/', 'level': 2},
        ])

    def test_does_not_write_any_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            main_file = os.path.join(tmp, "CleanABAP.md")
            write_file(main_file, "# Clean ABAP\n\nIntro.\n\n## Names\n\nSee [names](#names).\n")

            parse_main(main_file)

            self.assertEqual(os.listdir(tmp), ["CleanABAP.md"])


class ParseSubSectionsTests(unittest.TestCase):
    def test_returns_tuples_sorted_by_filename_with_deterministic_subsection_index_weight(self):
        with tempfile.TemporaryDirectory() as tmp:
            zzz = os.path.join(tmp, "ZzzTopic.md")
            aaa = os.path.join(tmp, "AaaTopic.md")
            write_file(zzz, "# Zzz Topic\n\nContent.\n")
            write_file(aaa, "# Aaa Topic\n\nContent.\n")

            parsed = parse_sub_sections([zzz, aaa])

        self.assertEqual([os.path.basename(p) for p, _, _, _ in parsed], ["AaaTopic.md", "ZzzTopic.md"])
        self.assertEqual(parsed[0][2].weight, 10)  # subsection_index 0 -> (0 + 1) * 10
        self.assertEqual(parsed[1][2].weight, 20)  # subsection_index 1 -> (1 + 1) * 10

    def test_heading_data_includes_own_root_under_its_deep_dives_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, "SomeTopic.md")
            write_file(f, "# Some Topic\n\nIntro.\n\n## Detail\n\nMore.\n")

            [(_file_path, folder_name, _tree, heading_data)] = parse_sub_sections([f])

        self.assertEqual(folder_name, "some-topic")
        self.assertEqual(heading_data, [
            {'text': 'Some Topic', 'path': '/clean-code/deep-dives/some-topic/', 'level': 1},
            {'text': 'Detail', 'path': '/clean-code/deep-dives/some-topic/detail/', 'level': 2},
        ])


class RunConversionCrossReferenceOrderTests(unittest.TestCase):
    def _run(self, main_content, sub_sections):
        with tempfile.TemporaryDirectory() as repo_root, tempfile.TemporaryDirectory() as output_dir:
            clean_abap_dir = os.path.join(repo_root, 'assets', 'sources', 'sap-styleguides', 'clean-abap')
            write_file(os.path.join(clean_abap_dir, 'CleanABAP.md'), main_content)
            for filename, content in sub_sections.items():
                write_file(os.path.join(clean_abap_dir, 'sub-sections', filename), content)

            run_conversion(repo_root, output_dir)

            generated = {}
            for root, _dirs, files in os.walk(output_dir):
                for fn in files:
                    path = os.path.join(root, fn)
                    with open(path, encoding='utf-8') as fh:
                        generated[os.path.relpath(path, output_dir)] = fh.read()
            return generated

    def test_main_file_link_to_a_subsection_only_heading_resolves(self):
        main_content = (
            "# Clean ABAP\n\n"
            "## Names\n\n"
            "See [encoding advice](#avoid-obscure-encodings) for details.\n"
        )
        sub_sections = {
            "AvoidEncodings.md": "# Avoid Obscure Encodings\n\nDon't use Hungarian notation.\n",
        }

        generated = self._run(main_content, sub_sections)
        names_content = generated[os.path.join('names', 'index.md')]

        self.assertIn('(/clean-code/deep-dives/avoid-encodings/)', names_content)

    def test_alphabetically_early_subsection_link_to_later_subsection_heading_resolves(self):
        main_content = "# Clean ABAP\n\n## Names\n\nUse descriptive names.\n"
        sub_sections = {
            "AaaTopic.md": "# Aaa Topic\n\nSee [zzz topic](#zzz-heading) for details.\n",
            "ZzzTopic.md": "# Zzz Topic\n\n## Zzz Heading\n\nSome content.\n",
        }

        generated = self._run(main_content, sub_sections)
        aaa_content = generated[os.path.join('deep-dives', 'aaa-topic', 'index.md')]

        self.assertIn('(/clean-code/deep-dives/zzz-topic/zzz-heading/)', aaa_content)

    def test_main_self_reference_is_not_hijacked_by_identically_titled_subsection_heading(self):
        main_content = (
            "# Clean ABAP\n\n"
            "## Error Handling\n\n"
            "See [exceptions](#exceptions) below.\n\n"
            "### Exceptions\n\nUse class-based exceptions.\n"
        )
        sub_sections = {
            "Exceptions.md": "# Exceptions\n\nDeep dive on exceptions.\n",
        }

        generated = self._run(main_content, sub_sections)
        error_handling_content = generated[os.path.join('error-handling', '_index.md')]

        self.assertIn('(/clean-code/error-handling/exceptions/)', error_handling_content)
        self.assertNotIn('/clean-code/deep-dives/exceptions/', error_handling_content)


if __name__ == '__main__':
    unittest.main()
