"""
Utility functions for Clean ABAP to Hugo conversion.
"""

import re
import os
from typing import List, Optional


def kebab_case(text: str) -> str:
    """
    Convert text to kebab-case.
    
    Rules:
    - Lowercase all characters
    - Replace spaces with hyphens
    - Insert hyphens before capital letters (for camelCase)
    - Remove all punctuation (commas, periods, apostrophes, parentheses, etc.)
    - Preserve existing hyphens
    
    Examples:
        "How to" -> "how-to"
        "Get Started with Clean Code" -> "get-started-with-clean-code"
        "Avoid encodings, esp. Hungarian notation" -> "avoid-encodings-esp-hungarian-notation"
        "InterfacesVsAbstractClasses" -> "interfaces-vs-abstract-classes"
    """
    # Insert hyphens before capital letters (for camelCase)
    text = re.sub(r'([a-z])([A-Z])', r'\1-\2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1-\2', text)
    
    # Remove punctuation and special characters (but preserve hyphens)
    text = re.sub(r'[\"\'`~!@#$%^&*()+={}\[\]|\\:;\"<>?,./\s]+', ' ', text)
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Trim and lowercase
    text = text.strip().lower()
    # Replace spaces with hyphens
    text = text.replace(' ', '-')
    # Remove any remaining non-alphanumeric (except hyphens)
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def clean_heading_text(text: str) -> str:
    """
    Clean heading text by removing markdown link syntax and other artifacts.
    
    Examples:
        "## [How to](#how-to)" -> "How to"
        "### Use descriptive names" -> "Use descriptive names"
    """
    # Remove markdown links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove heading markers
    text = re.sub(r'^#+\s*', '', text)
    # Trim whitespace
    return text.strip()


def get_heading_level(line: str) -> Optional[int]:
    """
    Get the heading level from a markdown line.
    Returns None if the line is not a heading.
    """
    match = re.match(r'^(#+)\s', line)
    if match:
        return len(match.group(1))
    return None


def extract_heading_text(line: str) -> Optional[str]:
    """
    Extract the text from a heading line.
    Returns None if the line is not a heading.
    """
    level = get_heading_level(line)
    if level is None:
        return None
    # Remove the heading markers and any leading/trailing whitespace
    text = re.sub(r'^#+\s*', '', line)
    return clean_heading_text(text)


def is_breadcrumb_line(line: str) -> bool:
    """
    Check if a line is a breadcrumb navigation line.
    Pattern: > [Clean ABAP](#clean-abap) > [Content](#content) > ...
    """
    return bool(re.match(r'^>\s*\[Clean ABAP\]', line))


def is_language_nav_block(lines: List[str], start_idx: int) -> bool:
    """
    Check if a block of lines is the language navigation block.
    Lines 3-17 in CleanABAP.md:
    > [**English**](CleanABAP.md)
    > &nbsp;·&nbsp;
    > [中文](CleanABAP_zh.md)
    ...
    """
    if start_idx >= len(lines):
        return False
    
    line = lines[start_idx]
    # Check for the English link pattern
    if '> [**English**](CleanABAP.md)' in line:
        return True
    return False


def is_toc_section(lines: List[str], start_idx: int) -> bool:
    """
    Check if we're at the start of the TOC section.
    The TOC starts with "## Content" and continues until the next "## " heading.
    """
    if start_idx >= len(lines):
        return False
    
    line = lines[start_idx]
    return line.strip() == '## Content'


def find_toc_end(lines: List[str], start_idx: int) -> int:
    """
    Find the end of the TOC section (next ## heading).
    """
    for i in range(start_idx + 1, len(lines)):
        if get_heading_level(lines[i]) == 2:
            return i
    return len(lines)


def remove_language_nav(lines: List[str]) -> List[str]:
    """
    Remove the language navigation block (lines 3-17).
    """
    result = []
    i = 0
    while i < len(lines):
        if i < len(lines) - 1 and '> [**English**](CleanABAP.md)' in lines[i]:
            # Skip until we find the blank line after the language nav
            i += 1
            while i < len(lines) and (lines[i].startswith('>') or lines[i].strip() == ''):
                i += 1
            continue
        result.append(lines[i])
        i += 1
    return result


def remove_breadcrumb_lines(lines: List[str]) -> List[str]:
    """
    Remove all breadcrumb navigation lines.
    Pattern: > [Clean ABAP](#clean-abap) > [Content](#content) > ...
    """
    return [line for line in lines if not is_breadcrumb_line(line)]


def remove_toc_section(lines: List[str]) -> List[str]:
    """
    Remove the entire TOC section (## Content until next ## heading).
    Also removes bullet-point TOC sections in sub-sections.
    """
    result = []
    i = 0
    in_toc = False
    in_bullet_toc = False
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if we're at the start of TOC (## Content)
        if get_heading_level(line) == 2 and 'Content' in clean_heading_text(line):
            in_toc = True
            i += 1
            continue
        
        # Check if we're at the start of a bullet-point TOC section
        # This appears in sub-sections like: - [Abstract](#abstract)
        # Look for a line that starts with "- [" and contains "](#" 
        if (stripped.startswith('- [') and '#' in stripped and 
            i > 0 and lines[i-1].strip() == '' and 
            not (i > 1 and lines[i-2].strip().startswith('- ['))):
            in_bullet_toc = True
            i += 1
            continue
        
        # If we're in TOC, check if we've reached the next ## heading
        if in_toc and get_heading_level(line) == 2:
            in_toc = False
            result.append(line)  # Keep the new heading
            i += 1
            continue
        
        # If we're in bullet TOC, check if we've reached a heading or end of TOC
        if in_bullet_toc:
            # Check if this is a heading (starts with #) - this ends the TOC
            if get_heading_level(line) is not None:
                in_bullet_toc = False
                result.append(line)  # Keep the heading
                i += 1
                continue
            # Check if this is another TOC bullet point
            elif stripped.startswith('- [') and '#' in stripped:
                # Still in TOC, skip it
                i += 1
                continue
            # Check if this is an empty line followed by a heading
            elif stripped == '' and i + 1 < len(lines) and get_heading_level(lines[i+1]) is not None:
                in_bullet_toc = False
                result.append(line)  # Keep the blank line
                i += 1
                continue
            else:
                # Keep the line but end TOC mode
                in_bullet_toc = False
                result.append(line)
                i += 1
                continue
        
        # Skip lines while in TOC
        if in_toc:
            i += 1
            continue
        
        result.append(line)
        i += 1
    
    return result


def remove_cheat_sheet_link(lines: List[str]) -> List[str]:
    """
    Remove the cheat sheet link line.
    Pattern: "The [Cheat Sheet](cheat-sheet/CheatSheet.md) is a print-optimized version."
    """
    return [line for line in lines if 'The [Cheat Sheet]' not in line]


def remove_back_to_guide_links(lines: List[str]) -> List[str]:
    """
    Remove the "Back to the guide" navigation links.
    Pattern: > [Back to the guide](../CleanABAP.md)
    """
    return [line for line in lines if '> [Back to the guide]' not in line]


def resolve_reference_links(lines: List[str]) -> List[str]:
    """
    Resolve reference-style markdown links to inline links.
    Reference-style links look like: [text][ref], [text][], or [text]
    Reference definitions look like: [ref]: url
    
    This function replaces reference-style links with inline links.
    """
    # First, collect all reference definitions
    references = {}
    
    for line in lines:
        # Match reference definition pattern: [id]: url
        # The id can contain various characters, and there may be optional whitespace
        match = re.match(r'^\[([^\]]+)\]\s*:\s*(.+?)\s*$', line)
        if match:
            ref_id = match.group(1)
            url = match.group(2).strip()
            references[ref_id] = url
    
    if not references:
        # No references to resolve, return original
        return lines
    
    # Now replace reference-style links in all lines
    result = []
    for line in lines:
        # Skip reference definition lines (they'll be removed anyway)
        if re.match(r'^\[([^\]]+)\]\s*:\s*', line):
            continue
        
        # Replace [text][ref] with [text](url)
        # Pattern 1: [text][ref] where ref is explicitly specified
        def replace_ref_link(match):
            link_text = match.group(1)
            ref_id = match.group(2)
            if ref_id in references:
                return f'[{link_text}]({references[ref_id]})'
            # If reference not found, keep original
            return match.group(0)
        
        line = re.sub(r'\[([^\]]+)\]\[([^\]]+)\]', replace_ref_link, line)
        
        # Pattern 2: [text][] where ref_id equals text
        def replace_implicit_ref_link(match):
            link_text = match.group(1)
            if link_text in references:
                return f'[{link_text}]({references[link_text]})'
            # If reference not found, keep original
            return match.group(0)
        
        line = re.sub(r'\[([^\]]+)\]\[\]', replace_implicit_ref_link, line)
        
        # Pattern 3: [text] when there's a reference definition for that exact text
        # This handles the shorthand form where [text] alone is treated as a link
        # We need to be careful to only replace this when it's NOT part of:
        # - [text](url) - inline link
        # - [text][ref] - reference link
        # - [text][] - implicit reference link
        # Use negative lookahead to avoid matching these cases
        def replace_shorthand_ref_link(match):
            link_text = match.group(1)
            if link_text in references:
                return f'[{link_text}]({references[link_text]})'
            # If reference not found, keep original
            return match.group(0)
        
        # Match [text] only if NOT followed by (, [, or ]
        # The pattern uses negative lookahead: (?![...])
        line = re.sub(r'\[([^\]]+)\](?![\]\(\[])', replace_shorthand_ref_link, line)
        
        result.append(line)
    
    return result


def clean_source_content(lines: List[str]) -> List[str]:
    """
    Apply all content cleaning steps:
    1. Resolve reference-style links to inline links
    2. Remove language navigation block
    3. Remove breadcrumb navigation lines
    4. Remove TOC section
    5. Remove cheat sheet link
    6. Remove "Back to the guide" links
    """
    lines = resolve_reference_links(lines)
    lines = remove_language_nav(lines)
    lines = remove_breadcrumb_lines(lines)
    lines = remove_toc_section(lines)
    lines = remove_cheat_sheet_link(lines)
    lines = remove_back_to_guide_links(lines)
    return lines


def ensure_directory(path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    """
    os.makedirs(path, exist_ok=True)
