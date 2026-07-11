"""
Main script for converting Clean ABAP markdown to Hugo content structure.
"""

import os
import re
import sys
import shutil
from typing import List, Dict, Tuple

from .utils import kebab_case, ensure_directory, load_link_titles
from .frontmatter import generate_front_matter, get_deep_dives_source_url
from .crossref import CrossReferenceConverter, build_path_mapping
from .tree import Page, parse_tree, resolve_links, apply_text_fixups, walk
from .writer import write_tree


def get_source_files(base_dir: str) -> Dict[str, str]:
    """
    Get the source files to process.
    
    Returns:
        Dictionary of file paths
    """
    clean_abap_path = os.path.join(
        base_dir, 
        'assets', 
        'sources', 
        'sap-styleguides', 
        'clean-abap', 
        'CleanABAP.md'
    )
    
    sub_sections_dir = os.path.join(
        base_dir, 
        'assets', 
        'sources', 
        'sap-styleguides', 
        'clean-abap', 
        'sub-sections'
    )
    
    sub_sections = []
    if os.path.exists(sub_sections_dir):
        for filename in os.listdir(sub_sections_dir):
            if filename.endswith('.md') and not filename.startswith('CleanABAP'):
                sub_sections.append(os.path.join(sub_sections_dir, filename))
    
    return {
        'main': clean_abap_path,
        'sub_sections': sub_sections
    }


def _heading_entry(page: Page, prefix_parts: List[str]) -> Dict:
    path = '/' + '/'.join(prefix_parts + page.path_parts)
    return {
        'text': page.title,
        'path': f"/clean-code{path}/",
        'level': page.level,
    }


def parse_main(main_file: str) -> Tuple[Page, List[Dict]]:
    """
    Parse the main CleanABAP.md file into a Page tree and extract its
    heading data for cross-reference mapping. Pure aside from reading the
    source file -- no link resolution, fixups, or writing happens here, so
    this can run before any other file's heading data exists.

    Returns:
        (tree, heading_data) -- heading_data excludes the site root itself,
        which is never addressable via a heading anchor.
    """
    print(f"Processing {main_file}...")

    with open(main_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    tree = parse_tree(markdown_text, is_subsection=False)

    heading_data = [
        _heading_entry(page, [])
        for child in tree.children
        for page in walk(child)
    ]

    return tree, heading_data


def parse_sub_sections(sub_section_files: List[str]) -> List[Tuple[str, str, Page, List[Dict]]]:
    """
    Parse every sub-section file into a Page tree and its heading data.
    Sorted by filename purely to keep subsection_index (and thus each
    sub-section's own weight) deterministic -- unrelated to cross-reference
    resolution, which now sees every file's heading data regardless of
    parse order (see write_sub_section).

    Returns:
        List of (file_path, folder_name, tree, heading_data) tuples, one
        per sub-section file, in sorted-filename order. heading_data
        includes the sub-section's own root heading (level 1), unlike the
        main content's root -- it's written directly into the sub-section's
        own base_dir (its path_parts is already [] -- see tree.parse_tree).
    """
    parsed = []

    for i, file_path in enumerate(sorted(sub_section_files)):
        filename = os.path.basename(file_path)
        print(f"Processing sub-section: {filename}...")

        folder_name = kebab_case(filename[:-3])  # Remove .md extension

        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        tree = parse_tree(markdown_text, is_subsection=True, subsection_index=i)
        heading_data = [_heading_entry(page, ['deep-dives', folder_name]) for page in walk(tree)]

        parsed.append((file_path, folder_name, tree, heading_data))

    return parsed


def _converter_for(own_heading_data: List[Dict], all_heading_data: List[Dict]) -> CrossReferenceConverter:
    """
    Build a converter that resolves against every parsed file's headings,
    but with own_heading_data appended last so a file's own headings always
    win ties for itself -- otherwise a same-titled heading in another file
    could silently hijack a same-file self-reference (real collisions exist
    in the source data, e.g. "Exceptions" appears both in CleanABAP.md and
    in a sub-section; see scripts/tests/test_main.py).
    """
    return CrossReferenceConverter(build_path_mapping(all_heading_data + own_heading_data))


def write_main(
    tree: Page,
    output_dir: str,
    main_file: str,
    own_heading_data: List[Dict],
    all_heading_data: List[Dict],
    link_titles: Dict[str, str],
) -> None:
    """Resolve links and fixups against the full cross-file mapping, then write the main content."""
    converter = _converter_for(own_heading_data, all_heading_data)
    tree = resolve_links(tree, converter)
    tree = apply_text_fixups(tree, is_subsection=False)

    file_count = write_tree(tree, output_dir, source_file=main_file, is_subsection=False, link_titles=link_titles)
    print(f"Generated {file_count} files from main content")


def write_sub_section(
    file_path: str,
    folder_name: str,
    tree: Page,
    output_dir: str,
    own_heading_data: List[Dict],
    all_heading_data: List[Dict],
    link_titles: Dict[str, str],
) -> None:
    """Resolve links and fixups against the full cross-file mapping, then write one sub-section."""
    filename = os.path.basename(file_path)
    subsection_base = os.path.join(output_dir, 'deep-dives', folder_name)
    ensure_directory(subsection_base)

    converter = _converter_for(own_heading_data, all_heading_data)
    tree = resolve_links(tree, converter)
    tree = apply_text_fixups(tree, is_subsection=True)

    file_count = write_tree(
        tree, subsection_base, source_file=file_path, is_subsection=True,
        content_root=output_dir, link_titles=link_titles,
    )
    print(f"Generated {file_count} files from {filename}")


def setup_output_dir(output_dir: str) -> None:
    """
    Clean up any existing generated content and recreate the output directory.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    ensure_directory(output_dir)


def run_conversion(repo_root: str, output_dir: str) -> None:
    """
    Run the full CleanABAP.md + sub-sections conversion into output_dir.
    """
    source_files = get_source_files(repo_root)

    if not os.path.exists(source_files['main']):
        print(f"Error: Main CleanABAP.md file not found at {source_files['main']}")
        sys.exit(1)

    print("Starting Clean ABAP to Hugo conversion...")
    print(f"Source: {source_files['main']}")
    print(f"Output: {output_dir}")
    print()

    # Parse every source file first, so cross-reference resolution has a
    # complete picture of every heading no matter which file references
    # which. Resolving before every file is parsed is what let links fall
    # through to CrossReferenceConverter's guessed-path fallback.
    main_tree, main_heading_data = parse_main(source_files['main'])
    sub_sections = parse_sub_sections(source_files['sub_sections'])

    all_heading_data = list(main_heading_data)
    for _file_path, _folder_name, _tree, heading_data in sub_sections:
        all_heading_data.extend(heading_data)

    link_titles = load_link_titles(repo_root)

    write_main(main_tree, output_dir, source_files['main'], main_heading_data, all_heading_data, link_titles)
    for file_path, folder_name, tree, heading_data in sub_sections:
        write_sub_section(file_path, folder_name, tree, output_dir, heading_data, all_heading_data, link_titles)

    # Create the deep-dives/_index.md file
    deep_dives_path = os.path.join(output_dir, 'deep-dives')
    ensure_directory(deep_dives_path)

    deep_dives_front_matter = generate_front_matter(
        title="Deep Dives",
        weight=190,
        source=get_deep_dives_source_url()
    )

    deep_dives_content = deep_dives_front_matter + "\nDeep dive articles on specific topics from the Clean ABAP styleguide.\n"

    with open(os.path.join(deep_dives_path, '_index.md'), 'w', encoding='utf-8') as f:
        f.write(deep_dives_content)


def find_internal_links(content: str) -> List[str]:
    """
    Extract internal /clean-code/... link targets from markdown content.
    """
    return [
        target for _text, target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        if target.startswith('/clean-code/')
    ]


def validate_cross_references(output_dir: str) -> List[Tuple[str, str]]:
    """
    Scan all generated markdown files for internal /clean-code/ links and
    check that each one resolves to a generated page.

    Returns:
        List of (source_file, broken_link) pairs.
    """
    broken = []

    for root, _dirs, files in os.walk(output_dir):
        for filename in files:
            if not filename.endswith('.md'):
                continue
            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for link in find_internal_links(content):
                # Link targets look like "/clean-code/names/use-descriptive-names/";
                # drop the leading "clean-code" segment since it's already output_dir.
                sub_parts = link.strip('/').split('/')[1:]
                target_dir = os.path.join(output_dir, *sub_parts) if sub_parts else output_dir
                if not (os.path.isfile(os.path.join(target_dir, 'index.md')) or
                        os.path.isfile(os.path.join(target_dir, '_index.md'))):
                    broken.append((file_path, link))

    return broken


def print_summary(output_dir: str) -> None:
    """
    Print a summary of the generated content.
    """
    total_files = 0
    for root, dirs, files in os.walk(output_dir):
        for filename in files:
            if filename == '_index.md':
                total_files += 1

    print(f"\nConversion complete!")
    print(f"Generated {total_files} content files in {output_dir}")


def main():
    """
    Main function to run the conversion.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    output_dir = os.path.join(repo_root, 'content', 'clean-code')

    setup_output_dir(output_dir)
    run_conversion(repo_root, output_dir)

    broken_links = validate_cross_references(output_dir)
    if broken_links:
        print(f"\nWarning: {len(broken_links)} internal link(s) do not resolve to a generated page:")
        for file_path, link in broken_links:
            print(f"  {os.path.relpath(file_path, output_dir)}: {link}")

    print_summary(output_dir)


if __name__ == '__main__':
    main()
