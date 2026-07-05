"""
Main script for converting Clean ABAP markdown to Hugo content structure.
"""

import os
import sys
import shutil
from typing import List, Dict, Any

# Add the scripts directory to the path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

from utils import (
    kebab_case, clean_source_content, ensure_directory
)
from frontmatter import generate_front_matter, get_source_url, get_root_source_url, get_deep_dives_source_url
from crossref import CrossReferenceConverter, build_path_mapping, create_converter_from_structure
from processor import ContentProcessor


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


def copy_images(source_dir: str, target_dir: str) -> int:
    """
    Copy PNG images from source to target directory.
    
    Args:
        source_dir: Source directory containing images
        target_dir: Target directory for images
    
    Returns:
        Number of images copied
    """
    if not os.path.exists(source_dir):
        return 0
    
    count = 0
    image_files = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
    
    for filename in os.listdir(source_dir):
        if any(filename.lower().endswith(ext) for ext in image_files):
            if not filename.endswith('.vsdx'):  # Skip Visio files
                source_path = os.path.join(source_dir, filename)
                target_path = os.path.join(target_dir, filename)
                shutil.copy2(source_path, target_path)
                count += 1
    
    return count


def process_clean_abap(
    main_file: str,
    output_dir: str,
    sub_section_data: List[Dict] = None
) -> List[Dict]:
    """
    Process the main CleanABAP.md file.
    
    Args:
        main_file: Path to CleanABAP.md
        output_dir: Base output directory (e.g., content/clean-code/)
        sub_section_data: Optional data from sub-sections for path mapping
    
    Returns:
        List of heading data for cross-reference mapping
    """
    print(f"Processing {main_file}...")
    
    # Create processor
    processor = ContentProcessor(
        base_path=output_dir,
        source_file=main_file,
        is_subsection=False
    )
    
    # Process the file
    structure, all_headings = processor.process_file()
    
    # Build path mapping for cross-references
    heading_data = []
    for heading in all_headings:
        path_parts = heading['path_parts']
        path = '/' + '/'.join(path_parts)
        heading_data.append({
            'text': heading['text'],
            'path': f"/clean-code{path}/",
            'level': heading['level']
        })
    
    # Add sub-section paths to the mapping
    if sub_section_data:
        heading_data.extend(sub_section_data)
    
    # Create converter
    converter = CrossReferenceConverter(build_path_mapping(heading_data))
    
    # Generate Hugo files
    file_count = processor.generate_hugo_files(converter)
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
        
        # Create processor for this sub-section
        processor = ContentProcessor(
            base_path=subsection_base,
            source_file=file_path,
            is_subsection=True,
            subsection_index=i  # Track the position among sub-sections
        )
        
        # Process the file
        structure, all_headings = processor.process_file()
        
        # Extract heading data for cross-references
        sub_heading_data = []
        for heading in all_headings:
            path_parts = heading['path_parts']
            path = '/' + '/'.join(['deep-dives', folder_name] + path_parts)
            sub_heading_data.append({
                'text': heading['text'],
                'path': f"/clean-code{path}/",
                'level': heading['level']
            })
        
        all_sub_heading_data.extend(sub_heading_data)
        
        # Build path mapping including main content
        all_heading_data = main_heading_data + all_sub_heading_data
        converter = CrossReferenceConverter(build_path_mapping(all_heading_data))
        
        # Generate Hugo files
        file_count = processor.generate_hugo_files(converter)
        print(f"Generated {file_count} files from {filename}")
    
    return all_sub_heading_data


def main():
    """
    Main function to run the conversion.
    """
    # Get the base directory (parent of this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    # Set up directories
    output_dir = os.path.join(repo_root, 'content', 'clean-code')
    
    # Clean up existing content
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    ensure_directory(output_dir)
    
    # Get source files
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
    else:
        sub_heading_data = []
    
    # Create the deep-dives/_index.md file
    deep_dives_path = os.path.join(output_dir, 'deep-dives')
    ensure_directory(deep_dives_path)
    
    deep_dives_front_matter = generate_front_matter(
        title="Deep Dives",
        weight=190,
        source=get_deep_dives_source_url(),
        date="2026-07-05"
    )
    
    deep_dives_content = deep_dives_front_matter + "\nDeep dive articles on specific topics from the Clean ABAP styleguide.\n"
    
    with open(os.path.join(deep_dives_path, '_index.md'), 'w', encoding='utf-8') as f:
        f.write(deep_dives_content)
    
    # Note: Images are now copied during content processing in the processor
    # Cross-references are also fixed during content processing
    
    # Print summary
    total_files = 0
    for root, dirs, files in os.walk(output_dir):
        for filename in files:
            if filename == '_index.md':
                total_files += 1
    
    print(f"\nConversion complete!")
    print(f"Generated {total_files} content files in {output_dir}")
    
    # Print folder structure
    print(f"\nFolder structure:")
    for root, dirs, files in os.walk(output_dir):
        level = root.replace(output_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")


if __name__ == '__main__':
    main()
