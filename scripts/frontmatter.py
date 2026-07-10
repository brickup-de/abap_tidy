"""
Front matter generation for Hugo content pages.
"""

from typing import Optional
from datetime import datetime

from .utils import kebab_case


def escape_yaml_string(value: str) -> str:
    """
    Escape a string for YAML double-quoted scalar.
    
    Args:
        value: The string to escape
    
    Returns:
        Escaped string safe for YAML double-quoted scalars
    """
    # Escape backslashes first (before other escapes)
    value = value.replace('\\', '\\\\')
    # Escape double quotes
    value = value.replace('"', '\\"')
    # Escape newlines
    value = value.replace('\n', '\\n')
    return value


def generate_front_matter(
    title: str,
    weight: int,
    source: str,
    date: Optional[str] = None,
    license: str = "CC BY 3.0",
    license_url: str = "https://creativecommons.org/licenses/by/3.0/"
) -> str:
    """
    Generate Hugo front matter in YAML format.
    
    Args:
        title: The page title
        weight: The page weight for sorting
        source: The source URL
        date: Optional date string (default: today's date)
        license: License name
        license_url: License URL
    
    Returns:
        YAML front matter string
    """
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    # Escape the title for YAML
    escaped_title = escape_yaml_string(title)
    
    front_matter = f"""---
title: "{escaped_title}"
weight: {weight}
date: {date}
params:
  license: "{license}"
  license_url: "{license_url}"
  source: "{source}"
---
"""
    return front_matter


def get_source_url(
    file_path: str,
    line_number: Optional[int] = None,
    is_subsection: bool = False,
    heading_text: Optional[str] = None
) -> str:
    """
    Generate source URL based on file path and heading anchor.
    
    Args:
        file_path: The source file path
        line_number: Optional line number (1-based) - for backward compatibility
        is_subsection: Whether this is from a sub-section file
        heading_text: Optional heading text for generating anchor
    
    Returns:
        Source URL string
    """
    base_url = "https://github.com/SAP/styleguides/blob/main/clean-abap/"
    
    if is_subsection:
        # Extract filename from path
        filename = file_path.split('/')[-1]
        url = f"{base_url}sub-sections/{filename}"
    else:
        url = f"{base_url}CleanABAP.md"
    
    # Use heading anchor instead of line number if heading text is provided
    if heading_text:
        # Generate GitHub anchor format (lowercase, spaces to hyphens, no special chars)
        anchor = kebab_case(heading_text)
        url += f"#{anchor}"
    elif line_number:
        # Fallback to line number format for backward compatibility
        url += f"#L{line_number}"
    
    return url


def get_deep_dives_source_url() -> str:
    """
    Get source URL for the deep-dives landing page.
    """
    return "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/"


def get_root_source_url() -> str:
    """
    Get source URL for the root clean-code page.
    """
    return "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#L1"
