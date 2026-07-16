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

from scripts.main import get_source_files, parse_main, parse_sub_sections, run_conversion, validate_cross_references


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def write_mapping_toml(repo_root, chapterize, keep, diagrams=None):
    chapterize_list = ', '.join(f'"{p}"' for p in chapterize)
    keep_list = ', '.join(f'"{p}"' for p in keep)
    text = f'[files]\nchapterize = [{chapterize_list}]\nkeep = [{keep_list}]\n'
    if diagrams:
        text += '\n[diagrams]\n'
        for filename, block in diagrams.items():
            text += f"\"{filename}\" = '''\n{block}'''\n"
    write_file(os.path.join(repo_root, 'data', 'mapping.toml'), text)


class GetSourceFilesTests(unittest.TestCase):
    def _clean_abap_dir(self, repo_root):
        return os.path.join(repo_root, 'assets', 'sources', 'sap-styleguides', 'clean-abap')

    def test_resolves_main_and_sub_sections_and_keep_files_from_config(self):
        with tempfile.TemporaryDirectory() as repo_root:
            clean_abap_dir = self._clean_abap_dir(repo_root)
            write_file(os.path.join(clean_abap_dir, 'CleanABAP.md'), '# Clean ABAP\n')
            write_file(os.path.join(clean_abap_dir, 'sub-sections', 'ModernABAPLanguageElements.md'), '# Modern\n')
            write_file(os.path.join(clean_abap_dir, 'sub-sections', 'AvoidEncodings.md'), '# Avoid Encodings\n')
            write_mapping_toml(
                repo_root,
                chapterize=['CleanABAP.md', 'sub-sections/ModernABAPLanguageElements.md'],
                keep=['sub-sections/AvoidEncodings.md'],
            )

            result = get_source_files(repo_root)

        self.assertEqual(result['main'], os.path.join(clean_abap_dir, 'CleanABAP.md'))
        self.assertEqual(
            set(result['sub_sections']),
            {
                os.path.join(clean_abap_dir, 'sub-sections', 'ModernABAPLanguageElements.md'),
                os.path.join(clean_abap_dir, 'sub-sections', 'AvoidEncodings.md'),
            },
        )
        self.assertEqual(
            result['keep_files'],
            {os.path.join(clean_abap_dir, 'sub-sections', 'AvoidEncodings.md')},
        )

    def test_raises_when_a_listed_file_does_not_exist_on_disk(self):
        with tempfile.TemporaryDirectory() as repo_root:
            clean_abap_dir = self._clean_abap_dir(repo_root)
            write_file(os.path.join(clean_abap_dir, 'CleanABAP.md'), '# Clean ABAP\n')
            write_mapping_toml(
                repo_root,
                chapterize=['CleanABAP.md'],
                keep=['sub-sections/DoesNotExist.md'],
            )

            with self.assertRaises(ValueError):
                get_source_files(repo_root)

    def test_raises_when_a_sub_section_file_on_disk_is_not_listed(self):
        with tempfile.TemporaryDirectory() as repo_root:
            clean_abap_dir = self._clean_abap_dir(repo_root)
            write_file(os.path.join(clean_abap_dir, 'CleanABAP.md'), '# Clean ABAP\n')
            write_file(os.path.join(clean_abap_dir, 'sub-sections', 'Unlisted.md'), '# Unlisted\n')
            write_mapping_toml(repo_root, chapterize=['CleanABAP.md'], keep=[])

            with self.assertRaises(ValueError):
                get_source_files(repo_root)

    def test_raises_when_no_main_file_is_listed_under_chapterize(self):
        with tempfile.TemporaryDirectory() as repo_root:
            clean_abap_dir = self._clean_abap_dir(repo_root)
            write_file(os.path.join(clean_abap_dir, 'sub-sections', 'AvoidEncodings.md'), '# Avoid Encodings\n')
            write_mapping_toml(repo_root, chapterize=['sub-sections/AvoidEncodings.md'], keep=[])

            with self.assertRaises(ValueError):
                get_source_files(repo_root)


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

    def test_heading_data_uses_dive_url_plus_fragment_for_keep_files(self):
        # A "keep" (single-page) dive has no nested directories to point at,
        # so every descendant heading maps to the dive's own URL plus a
        # #anchor fragment instead -- the root heading is unaffected.
        with tempfile.TemporaryDirectory() as tmp:
            f = os.path.join(tmp, "SomeTopic.md")
            write_file(f, "# Some Topic\n\nIntro.\n\n## Detail\n\nMore.\n")

            [(_file_path, folder_name, _tree, heading_data)] = parse_sub_sections([f], keep_files={f})

        self.assertEqual(folder_name, "some-topic")
        self.assertEqual(heading_data, [
            {'text': 'Some Topic', 'path': '/clean-code/deep-dives/some-topic/', 'level': 1},
            {'text': 'Detail', 'path': '/clean-code/deep-dives/some-topic/#detail', 'level': 2},
        ])


def run_conversion_for_test(main_content, sub_sections, keep=(), diagrams=None):
    with tempfile.TemporaryDirectory() as repo_root, tempfile.TemporaryDirectory() as output_dir:
        clean_abap_dir = os.path.join(repo_root, 'assets', 'sources', 'sap-styleguides', 'clean-abap')
        write_file(os.path.join(clean_abap_dir, 'CleanABAP.md'), main_content)
        for filename, content in sub_sections.items():
            write_file(os.path.join(clean_abap_dir, 'sub-sections', filename), content)
        write_mapping_toml(
            repo_root,
            chapterize=['CleanABAP.md'] + [f'sub-sections/{f}' for f in sub_sections if f not in keep],
            keep=[f'sub-sections/{f}' for f in keep],
            diagrams=diagrams,
        )

        run_conversion(repo_root, output_dir)

        generated = {}
        for root, _dirs, files in os.walk(output_dir):
            for fn in files:
                path = os.path.join(root, fn)
                with open(path, encoding='utf-8') as fh:
                    generated[os.path.relpath(path, output_dir)] = fh.read()
        return generated


class RunConversionCrossReferenceOrderTests(unittest.TestCase):
    def _run(self, main_content, sub_sections, keep=()):
        return run_conversion_for_test(main_content, sub_sections, keep)

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


class RunConversionKeepModeTests(unittest.TestCase):
    def test_keep_dive_renders_as_a_single_page_with_flattened_headings(self):
        main_content = "# Clean ABAP\n\n## Names\n\nUse descriptive names.\n"
        sub_sections = {
            "AvoidEncodings.md": (
                "# Avoid Encodings\n\nIntro.\n\n"
                "## Reasoning\n\nReasoning body.\n\n"
                "## Compromises\n\nCompromise body.\n"
            ),
        }

        generated = run_conversion_for_test(main_content, sub_sections, keep=("AvoidEncodings.md",))

        dive_prefix = os.path.join('deep-dives', 'avoid-encodings')
        dive_files = [p for p in generated if p.startswith(dive_prefix)]
        self.assertEqual(dive_files, [os.path.join(dive_prefix, 'index.md')])

        content = generated[os.path.join(dive_prefix, 'index.md')]
        self.assertIn('## Reasoning', content)
        self.assertIn('Reasoning body.', content)
        self.assertIn('## Compromises', content)
        self.assertIn('Compromise body.', content)
        self.assertLess(content.index('Reasoning body.'), content.index('## Compromises'))

    def test_link_to_a_subheading_inside_a_keep_dive_resolves_to_a_fragment(self):
        main_content = (
            "# Clean ABAP\n\n"
            "## Names\n\n"
            "See [encoding reasoning](#the-reasoning) for details.\n"
        )
        sub_sections = {
            "AvoidEncodings.md": "# Avoid Encodings\n\nIntro.\n\n## The Reasoning\n\nBody.\n",
        }

        generated = run_conversion_for_test(main_content, sub_sections, keep=("AvoidEncodings.md",))
        names_content = generated[os.path.join('names', 'index.md')]

        self.assertIn('(/clean-code/deep-dives/avoid-encodings/#the-reasoning)', names_content)

    def test_chapterize_dive_unaffected_by_an_unrelated_keep_dive(self):
        main_content = "# Clean ABAP\n\n## Names\n\nUse descriptive names.\n"
        sub_sections = {
            "AvoidEncodings.md": "# Avoid Encodings\n\nIntro.\n\n## Reasoning\n\nBody.\n",
            "Exceptions.md": "# Exceptions\n\nIntro.\n\n## The Ideal\n\nBody.\n",
        }

        generated = run_conversion_for_test(main_content, sub_sections, keep=("AvoidEncodings.md",))

        self.assertIn(os.path.join('deep-dives', 'exceptions', 'the-ideal', 'index.md'), generated)


class RunConversionDiagramOverrideTests(unittest.TestCase):
    def test_image_matching_a_diagrams_override_is_replaced_and_the_png_is_not_copied(self):
        main_content = "# Clean ABAP\n\n## Names\n\nUse descriptive names.\n"
        sub_section_content = "# Some Dive\n\nIntro.\n\n![](some-dive/Foo.png)\n\nMore text.\n"
        diagram_block = "```mermaid\nclassDiagram\n    A --> B\n```"

        with tempfile.TemporaryDirectory() as repo_root, tempfile.TemporaryDirectory() as output_dir:
            clean_abap_dir = os.path.join(repo_root, 'assets', 'sources', 'sap-styleguides', 'clean-abap')
            write_file(os.path.join(clean_abap_dir, 'CleanABAP.md'), main_content)
            write_file(os.path.join(clean_abap_dir, 'sub-sections', 'SomeDive.md'), sub_section_content)
            os.makedirs(os.path.join(clean_abap_dir, 'sub-sections', 'some-dive'))
            with open(os.path.join(clean_abap_dir, 'sub-sections', 'some-dive', 'Foo.png'), 'wb') as f:
                f.write(b'fake-image-bytes')
            write_mapping_toml(
                repo_root, chapterize=['CleanABAP.md'], keep=['sub-sections/SomeDive.md'],
                diagrams={'Foo.png': diagram_block},
            )

            run_conversion(repo_root, output_dir)

            dive_index = os.path.join(output_dir, 'deep-dives', 'some-dive', 'index.md')
            with open(dive_index, encoding='utf-8') as f:
                content = f.read()

        self.assertIn(diagram_block, content)
        self.assertNotIn('Foo.png', content)
        self.assertFalse(os.path.isfile(os.path.join(output_dir, 'deep-dives', 'some-dive', 'Foo.png')))


class ValidateCrossReferencesTests(unittest.TestCase):
    def test_fragment_link_to_an_existing_page_is_not_reported_as_broken(self):
        # A "keep" (single-page) dive's descendant headings resolve to
        # {dive-url}#{anchor} (see _heading_entry_single_page) -- an
        # in-page anchor, not a separate directory. The #fragment must be
        # stripped before checking whether the *page* exists, or every such
        # link would be a false-positive "broken link".
        with tempfile.TemporaryDirectory() as output_dir:
            write_file(
                os.path.join(output_dir, 'names', 'index.md'),
                "See [reasoning](/clean-code/deep-dives/avoid-encodings/#the-reasoning).\n",
            )
            write_file(os.path.join(output_dir, 'deep-dives', 'avoid-encodings', 'index.md'), "# Avoid Encodings\n")

            self.assertEqual(validate_cross_references(output_dir), [])

    def test_fragment_link_to_a_non_existing_page_is_still_reported_as_broken(self):
        with tempfile.TemporaryDirectory() as output_dir:
            write_file(
                os.path.join(output_dir, 'names', 'index.md'),
                "See [reasoning](/clean-code/deep-dives/does-not-exist/#the-reasoning).\n",
            )

            broken = validate_cross_references(output_dir)

        self.assertEqual(len(broken), 1)
        self.assertIn('/clean-code/deep-dives/does-not-exist/#the-reasoning', broken[0][1])

    def test_link_without_a_fragment_to_a_non_existing_page_is_still_reported_as_broken(self):
        with tempfile.TemporaryDirectory() as output_dir:
            write_file(
                os.path.join(output_dir, 'names', 'index.md'),
                "See [reasoning](/clean-code/deep-dives/does-not-exist/).\n",
            )

            broken = validate_cross_references(output_dir)

        self.assertEqual(len(broken), 1)


if __name__ == '__main__':
    unittest.main()
