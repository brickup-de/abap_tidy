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
    """
    result = []
    i = 0
    in_toc = False
    
    while i < len(lines):
        line = lines[i]
        
        # Check if we're at the start of TOC
        if get_heading_level(line) == 2 and 'Content' in clean_heading_text(line):
            in_toc = True
            i += 1
            continue
        
        # If we're in TOC, check if we've reached the next ## heading
        if in_toc and get_heading_level(line) == 2:
            in_toc = False
            result.append(line)  # Keep the new heading
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


def clean_source_content(lines: List[str]) -> List[str]:
    """
    Apply all content cleaning steps:
    1. Remove language navigation block
    2. Remove breadcrumb navigation lines
    3. Remove TOC section
    4. Remove cheat sheet link
    """
    lines = remove_language_nav(lines)
    lines = remove_breadcrumb_lines(lines)
    lines = remove_toc_section(lines)
    lines = remove_cheat_sheet_link(lines)
    return lines


def ensure_directory(path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.
    """
    os.makedirs(path, exist_ok=True)
