"""
Content processing module for Clean ABAP to Hugo conversion.
Handles parsing markdown files and splitting by heading hierarchy.
"""

import os
import shutil
import re
from typing import List, Dict, Tuple

from .utils import (
    get_heading_level, extract_heading_text, kebab_case,
    clean_source_content, ensure_directory
)
from .frontmatter import generate_front_matter, get_source_url, get_root_source_url
from .crossref import CrossReferenceConverter


class ContentProcessor:
    """
    Processes markdown content and generates Hugo-compatible structure.
    """
    
    def __init__(
        self,
        base_path: str,
        source_file: str,
        is_subsection: bool = False,
        parent_path: str = '',
        base_line: int = 1,
        subsection_index: int = 0
    ):
        """
        Initialize the content processor.
        
        Args:
            base_path: Base output path (e.g., content/clean-code/)
            source_file: Source markdown file path
            is_subsection: Whether this is a sub-section file
            parent_path: Parent path for nested content
            base_line: Base line number for source tracking
            subsection_index: Index of this sub-section among all sub-sections (for weight calculation)
        """
        self.base_path = base_path
        self.source_file = source_file
        self.is_subsection = is_subsection
        self.parent_path = parent_path
        self.base_line = base_line
        self.subsection_index = subsection_index
        
        # Track current state
        self.heading_stack = []
        self.current_content = []
        self.structure = []
        self.all_headings = []
    
    def process_file(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Process the markdown file and return structure and headings.
        
        Returns:
            Tuple of (structure, all_headings)
        """
        with open(self.source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Clean the content
        lines = clean_source_content(lines)
        
        # Initialize root content storage
        self.root_title = None
        self.root_content = None
        self.root_line = None
        
        # Process line by line
        self._process_lines(lines)
        
        return self.structure, self.all_headings
    
    def _process_lines(self, lines: List[str]) -> None:
        """
        Process lines to build the content structure.
        """
        current_level = 0
        current_path = []
        content_buffer = []
        
        for i, line in enumerate(lines):
            line_num = self.base_line + i + 1  # +1 for 1-based indexing
            heading_level = get_heading_level(line)
            
            if heading_level is not None:
                # We found a heading - save previous content
                if content_buffer and self.heading_stack:
                    # Content belongs to the current heading in the stack
                    current_heading_level = self.heading_stack[-1]['level']
                    current_heading_path = self.heading_stack[-1]['path_parts']
                    self._save_content(
                        ''.join(content_buffer),
                        current_heading_level,
                        current_heading_path,
                        line_num - len(content_buffer)  # Approximate start line
                    )
                    content_buffer = []
                
                # Handle the new heading
                heading_text = extract_heading_text(line)
                if heading_text:
                    # Close higher-level headings
                    while self.heading_stack and self.heading_stack[-1]['level'] >= heading_level:
                        self.heading_stack.pop()
                    
                    # Create folder name
                    folder_name = kebab_case(heading_text)
                    
                    # Build path
                    if self.heading_stack:
                        parent = self.heading_stack[-1]
                        if parent['level'] == 1:
                            # Don't include level 1 in path (it's the root)
                            # For sub-sections, level 1 headings are the main content
                            if self.is_subsection:
                                path_parts = [folder_name]
                            else:
                                path_parts = [folder_name]
                        else:
                            path_parts = parent['path_parts'] + [folder_name]
                    else:
                        # First heading in the file
                        if self.is_subsection:
                            # For sub-sections, level 1 is the main heading
                            path_parts = [folder_name]
                        else:
                            path_parts = [folder_name]
                    
                    # Add to stack
                    self.heading_stack.append({
                        'level': heading_level,
                        'text': heading_text,
                        'folder': folder_name,
                        'path_parts': path_parts,
                        'line': line_num
                    })
                    
                    current_level = heading_level
                    current_path = path_parts.copy()
                
                continue
            
            # Accumulate content for current section
            content_buffer.append(line)
        
        # Save any remaining content
        if content_buffer:
            self._save_content(
                ''.join(content_buffer),
                current_level,
                current_path,
                line_num - len(content_buffer) + 1
            )
    
    def _save_content(
        self,
        content: str,
        level: int,
        path_parts: List[str],
        start_line: int
    ) -> None:
        """
        Save accumulated content to the appropriate section.
        """
        if not self.heading_stack:
            return
        
        current_heading = self.heading_stack[-1]
        actual_level = current_heading['level']  # This is the level of the heading the content belongs to
        
        # Store heading information
        heading_info = {
            'text': current_heading['text'],
            'folder': current_heading['folder'],
            'level': actual_level,
            'path_parts': current_heading['path_parts'],
            'line': current_heading['line'],
            'content': content.strip(),
            'start_line': start_line
        }
        
        # For level 1 (main title), store as root content
        # But for sub-sections, level 1 should be treated as a regular heading
        if actual_level == 1 and not self.is_subsection:
            if not hasattr(self, 'root_title') or not self.root_title:
                self.root_title = current_heading['text']
                self.root_content = content.strip()
                self.root_line = current_heading['line']
        else:
            # For all other cases (including sub-sections level 1 and non-root level 1), add to all_headings
            self.all_headings.append(heading_info)
            
            # Add to structure based on level
            if actual_level == 1:
                # For sub-sections, level 1 becomes a top-level heading in the structure
                # This will be placed under the sub-section folder
                self.structure.append(heading_info)
            elif actual_level == 2:
                # For main content, level 2 goes to root structure
                # For sub-sections, level 2 should be children of level 1
                if self.is_subsection:
                    # Find the level 1 parent (should be the first item in structure for sub-sections)
                    for item in reversed(self.structure):
                        if item['level'] == 1:
                            if 'children' not in item:
                                item['children'] = []
                            item['children'].append(heading_info)
                            break
                else:
                    # For main content, add to root structure
                    self.structure.append(heading_info)
            else:
                # Nested heading - find parent and add as child
                parent_level = actual_level - 1
                for item in reversed(self.structure):
                    if item['level'] == parent_level:
                        if 'children' not in item:
                            item['children'] = []
                        item['children'].append(heading_info)
                        break
    
    def generate_hugo_files(self, converter: CrossReferenceConverter) -> int:
        """
        Generate Hugo content files from the processed structure.
        
        Args:
            converter: CrossReferenceConverter for link conversion
        
        Returns:
            Number of files generated
        """
        count = 0
        
        # Handle the root _index.md
        if not self.is_subsection:
            count += self._generate_root_file(converter)
        
        # Process all headings
        for heading in self.all_headings:
            count += self._generate_heading_file(heading, converter)
        
        return count
    
    def _generate_root_file(self, converter: CrossReferenceConverter) -> int:
        """
        Generate the root _index.md file for Clean ABAP.
        """
        # Use the stored root title and content
        title = getattr(self, 'root_title', 'Clean ABAP')
        intro_content = getattr(self, 'root_content', '')
        
        # Generate front matter
        source_url = get_root_source_url()
        front_matter = generate_front_matter(
            title=title,
            weight=1,
            source=source_url
        )
        
        # Create the content
        content = front_matter
        if intro_content:
            content += f"\n{converter.convert_content(intro_content)}\n"
        
        # Write to file
        output_path = os.path.join(self.base_path, '_index.md')
        ensure_directory(self.base_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return 1
    
    def _has_children(self, heading: Dict) -> bool:
        """
        Check if a heading has children in the structure.
        
        Args:
            heading: The heading to check
            
        Returns:
            True if the heading has children, False otherwise
        """
        # Check if this heading exists in the structure and has children
        for item in self.structure:
            if item['path_parts'] == heading['path_parts']:
                return 'children' in item and len(item['children']) > 0
        
        # For headings not in structure (like level 3+), check if there are any other headings
        # that have this heading's path as a prefix (indicating they are children)
        for other_heading in self.all_headings:
            if (other_heading != heading and 
                other_heading['path_parts'] and heading['path_parts'] and
                len(other_heading['path_parts']) > len(heading['path_parts']) and
                other_heading['path_parts'][:len(heading['path_parts'])] == heading['path_parts']):
                return True
        
        return False

    def _generate_heading_file(
        self,
        heading: Dict,
        converter: CrossReferenceConverter
    ) -> int:
        """
        Generate a Hugo file for a heading.
        Leaf pages (without children) are named index.md, 
        non-leaf pages (with children) are named _index.md.
        """
        # Build the path
        if self.is_subsection:
            # For sub-sections, the base_path already includes the sub-section folder
            # For level 1 headings, we want to create the file in the base_dir
            # For level 2+ headings, we want to create subfolders
            if heading['level'] == 1:
                # Level 1 heading content goes in base_dir/
                base_dir = self.base_path
                path_parts = []
            else:
                # Level 2+ headings go in subfolders
                base_dir = self.base_path
                path_parts = heading['path_parts']
        else:
            base_dir = self.base_path
            path_parts = heading['path_parts']
        
        folder_path = os.path.join(base_dir, *path_parts)
        
        # Calculate weight
        # For main CleanABAP.md: weight = (position among siblings) * 10
        # For sub-sections: different scheme
        if self.is_subsection:
            # For sub-sections, we need to calculate based on position
            # This will be handled by the main processor
            weight = self._calculate_weight(heading, self.structure)
        else:
            weight = self._calculate_weight(heading, self.structure)
        
        # Special case: deep-dives/_index.md
        if self.is_subsection and heading['text'] == 'Interfaces vs. Abstract Classes':
            if len(path_parts) == 1 and path_parts[0] == 'deep-dives':
                # This is the deep-dives landing page
                content = "Deep dive articles on specific topics from the Clean ABAP styleguide."
                front_matter = generate_front_matter(
                    title="Deep Dives",
                    weight=190,
                    source=get_source_url(
                        self.source_file,
                        is_subsection=True
                    ) + '/'
                )
                output_path = os.path.join(self.base_path, 'deep-dives', '_index.md')
                ensure_directory(os.path.join(self.base_path, 'deep-dives'))
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(front_matter + "\n" + content + "\n")
                return 1
        
        # Generate front matter
        source_url = get_source_url(
            self.source_file,
            line_number=heading['line'],
            is_subsection=self.is_subsection,
            heading_text=heading['text']
        )
        
        front_matter = generate_front_matter(
            title=heading['text'],
            weight=weight,
            source=source_url
        )
        
        # Convert cross-references in content
        converted_content = converter.convert_content(heading['content'])
        
        # Fix image references in the converted content
        fixed_content = self._fix_image_references(converted_content, folder_path)
        
        # Fix 'below' references that are now inaccurate after content splitting
        fixed_content = self._fix_below_references(fixed_content)
        
        # Create the full content
        content = front_matter
        if fixed_content:
            content += f"\n{fixed_content}\n"
        
        # Determine filename based on whether this is a leaf or non-leaf page
        # Leaf pages (without children) use index.md, non-leaf pages use _index.md
        has_children = self._has_children(heading)
        filename = '_index.md' if has_children else 'index.md'
        
        # Write to file
        ensure_directory(folder_path)
        output_path = os.path.join(folder_path, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Copy images referenced in the content to the target folder
        self._copy_images_for_content(folder_path, heading['content'])
        
        return 1
    
    def _fix_image_references(self, content: str, folder_path: str) -> str:
        """
        Fix image references in content to use relative paths.
        
        Args:
            content: Markdown content with image references
            folder_path: The folder where the content will be written
        
        Returns:
            Content with fixed image references
        """
        # Find all image references
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        def fix_image_reference(match):
            alt_text = match.group(1)
            image_path = match.group(2)
            
            # Skip if it's already a URL or absolute path
            if image_path.startswith('http://') or image_path.startswith('https://') or image_path.startswith('/'):
                return match.group(0)
            
            # Extract filename from the path
            filename = os.path.basename(image_path)
            
            # Convert to relative path (just the filename)
            return f"![{alt_text}]({filename})"
        
        # Replace all image references
        return re.sub(image_pattern, fix_image_reference, content)
    
    def _fix_below_references(self, content: str) -> str:
        """
        Fix references to 'below' that are now inaccurate after content splitting.
        """
        content = re.sub(
            r'\b(suggestions)\s+below\b',
            r'\1 on this site',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'\b(recommendations)\s+below\b',
            r'\1 on this site',
            content,
            flags=re.IGNORECASE
        )
        
        content = re.sub(
            r'\b(detailed\s+)?rules\s+below\b',
            r'related rules',
            content,
            flags=re.IGNORECASE
        )
        
        return content

    def _copy_images_for_content(self, target_folder: str, content: str) -> None:
        """
        Copy images referenced in content to the target folder.
        
        Args:
            target_folder: Target folder where images should be copied
            content: Markdown content that may contain image references
        """
        # Only copy images for sub-sections that have image directories
        if not self.is_subsection:
            return
        
        # Get the source directory for images
        # For sub-sections, images are typically in a folder next to the markdown file
        source_dir = os.path.dirname(self.source_file)
        
        # Find all image references in the content
        image_refs = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', content)
        
        for image_path in image_refs:
            # Extract filename from path
            filename = os.path.basename(image_path)
            
            # Only copy common image files
            if not any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']):
                continue
            if filename.endswith('.vsdx'):  # Skip Visio files
                continue
            
            # Try to find the image in the source directory or its subdirectories
            source_path = None
            
            # First, try the full path from the reference
            full_source_path = os.path.join(source_dir, image_path)
            if os.path.exists(full_source_path):
                source_path = full_source_path
            else:
                # Try just the filename in the source directory
                test_source_path = os.path.join(source_dir, filename)
                if os.path.exists(test_source_path):
                    source_path = test_source_path
                else:
                    # Search recursively in the source directory
                    for root, dirs, files in os.walk(source_dir):
                        if filename in files:
                            source_path = os.path.join(root, filename)
                            break
            
            if source_path and os.path.exists(source_path):
                target_path = os.path.join(target_folder, filename)
                ensure_directory(target_folder)
                shutil.copy2(source_path, target_path)
    
    def _calculate_weight(self, heading: Dict, structure: List[Dict]) -> int:
        """
        Calculate the weight for a heading based on its position among siblings.
        
        Rules:
        - Root _index.md: weight 1
        - First ## chapter: weight 10
        - Second ## chapter: weight 20
        - First ### under a parent: weight 10
        - Second ### under same parent: weight 20
        - deep-dives/_index.md: weight 190 (19th sibling in clean-code/)
        - First deep-dives sub-section: weight 10 (1st child in deep-dives/)
        - Second deep-dives sub-section: weight 20
        """
        if self.is_subsection:
            # For sub-sections, the base weight is determined by the sub-section index
            base_weight = (self.subsection_index + 1) * 10
            
            # For top-level sub-section headings (level 1), use the base weight
            if len(heading['path_parts']) == 0:
                return base_weight
            elif len(heading['path_parts']) == 1:
                # This is a level 1 heading (the main heading of the sub-section file)
                return base_weight
            else:
                # Nested heading within a sub-section
                # Find siblings at the same level
                parent_path = heading['path_parts'][:-1]
                for item in structure:
                    if item['path_parts'] == parent_path and 'children' in item:
                        siblings = item['children']
                        for i, sibling in enumerate(siblings):
                            if sibling['text'] == heading['text']:
                                return (i + 1) * 10
                        return 10
                return 10
        
        # For main content
        level = heading['level']
        
        # Find siblings at the same level
        if level == 2:
            # Top-level chapters
            siblings = [item for item in structure if item['level'] == 2]
            for i, sibling in enumerate(siblings):
                if sibling['text'] == heading['text']:
                    return (i + 1) * 10
            return 10
        
        # For nested headings, find parent and siblings
        parent_path = heading['path_parts'][:-1]
        for item in structure:
            if item['path_parts'] == parent_path and 'children' in item:
                siblings = item['children']
                for i, sibling in enumerate(siblings):
                    if sibling['text'] == heading['text']:
                        return (i + 1) * 10
                return 10
        
        return 10  # Default weight
