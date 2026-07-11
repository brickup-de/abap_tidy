"""
Cross-reference conversion for Hugo content.
Converts markdown anchor links to absolute Hugo paths.
"""

import re
from typing import List, Dict

from .utils import kebab_case


class CrossReferenceConverter:
    """
    Converts markdown anchor links to Hugo absolute paths.
    Maintains a mapping of heading text to paths for reference resolution.
    """

    # Matches relative links to markdown source files, e.g.:
    #   CleanABAP.md, ../CleanABAP.md#some-anchor,
    #   sub-sections/Enumerations.md, ../CONTRIBUTING.md
    FILE_LINK_PATTERN = re.compile(
        r'^(\.\./)?(?:(sub-sections)/)?([\w-]+)\.md(#.*)?$'
    )

    def __init__(self, path_mapping: Dict[str, str]):
        """
        Initialize with a mapping of heading text to paths.
        
        Args:
            path_mapping: Dictionary mapping heading text (lowercase) to Hugo paths
        """
        self.path_mapping = path_mapping
        self.conversion_cache = {}
    
    def convert_link(self, match: re.Match) -> str:
        """
        Convert a single markdown link match to Hugo path.
        
        Args:
            match: Regex match object with groups (text, anchor)
        
        Returns:
            Converted link string
        """
        link_text = match.group(1)
        anchor = match.group(2)
        
        # If it's already an absolute path, keep it
        if anchor.startswith('/') or anchor.startswith('http'):
            return match.group(0)

        # Handle links that point at a source markdown file rather than a
        # bare #anchor, e.g. "sub-sections/Enumerations.md" or
        # "../CleanABAP.md#prefer-composition-to-inheritance".
        file_match = self.FILE_LINK_PATTERN.match(anchor)
        if file_match:
            up_dir, subdir, filename, fragment = file_match.groups()
            fragment_anchor = fragment[1:] if fragment else None

            if filename == 'CleanABAP':
                # Link into the main guide - resolve via the fragment if
                # present, otherwise point at the guide's root page.
                if fragment_anchor is None:
                    return f"[{link_text}](/clean-code/)"
                anchor = fragment_anchor
            elif subdir == 'sub-sections':
                # Link into a sub-section (deep-dive) file.
                if fragment_anchor is None:
                    folder = kebab_case(filename)
                    return f"[{link_text}](/clean-code/deep-dives/{folder}/)"
                anchor = fragment_anchor
            else:
                # Reference to a file outside the generated content (e.g.
                # "../CONTRIBUTING.md"); link to the source on GitHub.
                base = "https://github.com/SAP/styleguides/blob/main/"
                rel_path = f"{filename}.md" if up_dir else f"clean-abap/{filename}.md"
                url = f"{base}{rel_path}"
                if fragment_anchor:
                    url += f"#{fragment_anchor}"
                return f"[{link_text}]({url})"
        elif anchor.startswith('#'):
            anchor = anchor[1:]
        
        # Look up the anchor in our path mapping
        # Try exact match first
        if anchor in self.path_mapping:
            hugo_path = self.path_mapping[anchor]
            return f"[{link_text}]({hugo_path})"
        
        # Try kebab-case version
        kebab_anchor = kebab_case(anchor)
        if kebab_anchor in self.path_mapping:
            hugo_path = self.path_mapping[kebab_anchor]
            return f"[{link_text}]({hugo_path})"
        
        # Try to find the closest match
        # This handles cases where the anchor might be slightly different
        for heading, path in self.path_mapping.items():
            if kebab_case(heading) == kebab_anchor:
                return f"[{link_text}]({path})"
        
        # If we can't find a match, try to construct a reasonable path
        # This is a fallback for references we couldn't map
        path_parts = kebab_anchor.split('-')
        if path_parts:
            # Try to find the best parent match
            for i in range(len(path_parts), 0, -1):
                candidate = '-'.join(path_parts[:i])
                if candidate in self.path_mapping:
                    base_path = self.path_mapping[candidate]
                    remaining = '-'.join(path_parts[i:])
                    if remaining:
                        return f"[{link_text}]({base_path}{remaining}/)"
                    return f"[{link_text}]({base_path})"
        
        # Last resort: return original link but with /clean-code/ prefix
        # This handles external links or links we can't resolve
        if anchor.startswith('http') or anchor.startswith('/'):
            return match.group(0)
        
        # For internal links that we couldn't resolve, use a reasonable default
        return f"[{link_text}](/clean-code/{kebab_anchor}/)"
    
    def convert_content(self, content: str) -> str:
        """
        Convert all markdown links in content to Hugo paths.
        
        Args:
            content: Markdown content with links
        
        Returns:
            Content with converted links
        """
        # Pattern for markdown links: [text](url)
        # We want to catch both absolute and relative links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        
        # Convert all links
        result = re.sub(link_pattern, self.convert_link, content)
        
        return result
    
def build_path_mapping(headings_data: List[Dict]) -> Dict[str, str]:
    """
    Build a mapping from heading text to Hugo paths.
    
    Args:
        headings_data: List of dictionaries with 'text', 'path', 'level' keys
    
    Returns:
        Dictionary mapping heading text (and kebab-case) to paths
    """
    mapping = {}
    
    for heading in headings_data:
        text = heading['text']
        path = heading['path']
        
        # Add exact text mapping
        mapping[text.lower()] = path
        
        # Add kebab-case mapping
        kebab_text = kebab_case(text)
        mapping[kebab_text] = path
        
        # Add text with # prefix (for anchor links)
        mapping[f'#{kebab_text}'] = path
        
        # Add lowercase kebab-case
        mapping[kebab_text.lower()] = path
    
    return mapping
