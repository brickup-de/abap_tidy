"""
Main script for converting Clean ABAP markdown to Hugo content structure.
"""

import os
import re
import sys
import shutil
from typing import List, Dict, Tuple

from .utils import kebab_case, ensure_directory
from .frontmatter import generate_front_matter, get_deep_dives_source_url
from .crossref import CrossReferenceConverter, build_path_mapping
from .tree import parse_tree, resolve_links, apply_text_fixups, walk
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


def process_clean_abap(
    main_file: str,
    output_dir: str
) -> List[Dict]:
    """
    Process the main CleanABAP.md file.

    Args:
        main_file: Path to CleanABAP.md
        output_dir: Base output directory (e.g., content/clean-code/)

    Returns:
        List of heading data for cross-reference mapping
    """
    print(f"Processing {main_file}...")

    with open(main_file, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    tree = parse_tree(markdown_text, is_subsection=False)

    # Build path mapping for cross-references. The site root itself is never
    # part of the mapping -- it isn't addressable via a heading anchor.
    heading_data = []
    for child in tree.children:
        for page in walk(child):
            path = '/' + '/'.join(page.path_parts)
            heading_data.append({
                'text': page.title,
                'path': f"/clean-code{path}/",
                'level': page.level
            })

    # Create converter
    converter = CrossReferenceConverter(build_path_mapping(heading_data))
    tree = resolve_links(tree, converter)
    tree = apply_text_fixups(tree, is_subsection=False)

    # Generate Hugo files
    file_count = write_tree(tree, output_dir, source_file=main_file, is_subsection=False)
    print(f"Generated {file_count} files from main content")

    return heading_data


def process_sub_sections(
    sub_section_files: List[str],
    output_dir: str,
    main_heading_data: List[Dict]
) -> List[Dict]:
    """
    Process the sub-section files.
    
    Args:
        sub_section_files: List of sub-section file paths
        output_dir: Base output directory
        main_heading_data: Heading data from main file for cross-references
    
    Returns:
        List of heading data from sub-sections
    """
    all_sub_heading_data = []
    
    # Sort sub-sections by filename for consistent ordering
    sorted_files = sorted(sub_section_files)
    
    for i, file_path in enumerate(sorted_files):
        filename = os.path.basename(file_path)
        print(f"Processing sub-section: {filename}...")
        
        # Create folder name from filename (without .md)
        folder_name = kebab_case(filename[:-3])  # Remove .md extension
        subsection_base = os.path.join(output_dir, 'deep-dives', folder_name)
        ensure_directory(subsection_base)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        tree = parse_tree(markdown_text, is_subsection=True, subsection_index=i)

        # Extract heading data for cross-references. The sub-section's own
        # root heading (level 1) is written directly into the sub-section's
        # base_dir (its path_parts is already [] -- see tree.parse_tree), so
        # it's included here too, unlike the main content's root.
        sub_heading_data = []
        for page in walk(tree):
            path = '/' + '/'.join(['deep-dives', folder_name] + page.path_parts)
            sub_heading_data.append({
                'text': page.title,
                'path': f"/clean-code{path}/",
                'level': page.level
            })

        all_sub_heading_data.extend(sub_heading_data)

        # Build path mapping including main content
        all_heading_data = main_heading_data + all_sub_heading_data
        converter = CrossReferenceConverter(build_path_mapping(all_heading_data))
        tree = resolve_links(tree, converter)
        tree = apply_text_fixups(tree, is_subsection=True)

        # Generate Hugo files
        file_count = write_tree(tree, subsection_base, source_file=file_path, is_subsection=True)
        print(f"Generated {file_count} files from {filename}")
    
    return all_sub_heading_data


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

    # Process main CleanABAP.md file first
    main_heading_data = process_clean_abap(
        source_files['main'],
        output_dir
    )

    # Process sub-sections
    if source_files['sub_sections']:
        sub_heading_data = process_sub_sections(
            source_files['sub_sections'],
            output_dir,
            main_heading_data
        )

        # Update main heading data with sub-section data
        main_heading_data.extend(sub_heading_data)

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

    # Note: Images are copied during content processing in the processor
    # Cross-references are also fixed during content processing


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
