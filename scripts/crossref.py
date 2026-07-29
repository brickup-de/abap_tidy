"""
Cross-reference conversion for Hugo content.
Converts markdown anchor links to absolute Hugo paths.
"""

import re
from typing import List, Dict, Optional

from .utils import kebab_case, github_anchor


def _by_exact_anchor(anchor: str, mapping: Dict[str, str]) -> Optional[str]:
    """Anchor matches a path_mapping key verbatim."""
    return mapping.get(anchor)


def _by_closest_heading(kebab_anchor: str, heading_cache: Dict[str, str]) -> Optional[str]:
    """Anchor's GitHub-anchor form matches some heading's, via a precomputed cache."""
    return heading_cache.get(kebab_anchor)


def _by_prefix(kebab_anchor: str, mapping: Dict[str, str]) -> Optional[str]:
    """Longest hyphen-separated prefix of the anchor that matches a mapping key."""
    path_parts = kebab_anchor.split('-')
    for i in range(len(path_parts), 0, -1):
        candidate = '-'.join(path_parts[:i])
        if candidate in mapping:
            base_path = mapping[candidate]
            remaining = '-'.join(path_parts[i:])
            return f"{base_path}{remaining}/" if remaining else base_path
    return None


def _guessed_fallback(kebab_anchor: str) -> str:
    """Last resort: construct a path from the anchor even if it was never seen."""
    return f"/{kebab_anchor}/"


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
        self.conversion_cache: Optional[Dict[str, str]] = None

    def convert_link(self, link_text: str, anchor: str) -> str:
        """
        Convert a single markdown link's text/anchor to a Hugo path.

        Args:
            link_text: The markdown link's visible text
            anchor: The markdown link's target (raw, before any resolution)

        Returns:
            Converted link string
        """
        # If it's already an absolute path, keep it
        if anchor.startswith('/') or anchor.startswith('http'):
            return f"[{link_text}]({anchor})"

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
                    return f"[{link_text}](/)"
                anchor = fragment_anchor
            elif subdir == 'sub-sections':
                # Link into a sub-section (deep-dive) file.
                if fragment_anchor is None:
                    folder = kebab_case(filename)
                    return f"[{link_text}](/deep-dives/{folder}/)"
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

        return f"[{link_text}]({self._resolve_anchor(anchor)})"

    def _resolve_anchor(self, anchor: str) -> str:
        """
        Resolve a bare anchor to a Hugo path, trying each strategy in order
        until one succeeds. The last strategy always succeeds.
        """
        kebab_anchor = github_anchor(anchor)
        return (
            _by_exact_anchor(anchor, self.path_mapping)
            or _by_exact_anchor(kebab_anchor, self.path_mapping)
            or _by_closest_heading(kebab_anchor, self._heading_cache())
            or _by_prefix(kebab_anchor, self.path_mapping)
            or _guessed_fallback(kebab_anchor)
        )

    def _heading_cache(self) -> Dict[str, str]:
        """
        Lazily build and memoize a github_anchor(heading) -> path lookup for
        every heading in path_mapping, so the closest-heading strategy is an
        O(1) lookup instead of an O(n) recompute on every call. First heading
        to produce a given anchor wins, matching the original linear scan.
        """
        if self.conversion_cache is None:
            cache: Dict[str, str] = {}
            for heading, path in self.path_mapping.items():
                cache.setdefault(github_anchor(heading), path)
            self.conversion_cache = cache
        return self.conversion_cache

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
        result = re.sub(
            link_pattern,
            lambda match: self.convert_link(match.group(1), match.group(2)),
            content
        )

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

        # Add GitHub-anchor mapping
        kebab_text = github_anchor(text)
        mapping[kebab_text] = path
        
        # Add text with # prefix (for anchor links)
        mapping[f'#{kebab_text}'] = path
        
        # Add lowercase kebab-case
        mapping[kebab_text.lower()] = path
    
    return mapping
