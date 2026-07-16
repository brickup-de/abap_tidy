"""
Pure "markdown text in, page tree out" stages for Clean ABAP -> Hugo
conversion. No filesystem access happens anywhere in this module; see
scripts/writer.py for the thin adapter that actually writes files.

Three composable stages, run in order by scripts/main.py:
  parse_tree        markdown text -> Page tree (structure, weight, has_children)
  resolve_links     rewrites cross-reference links via a CrossReferenceConverter
  apply_text_fixups rewrites image paths and stale "below" references

They're kept separate because resolve_links is the only stage that needs
state external to the single file being parsed (a converter built from
every file's heading data, parsed up front across the whole multi-file
pipeline run -- see scripts/main.py's parse_main/parse_sub_sections/
write_main/write_sub_section split). parse_tree and apply_text_fixups
depend on nothing but the file's own text.

One behavior is deliberately preserved from the ContentProcessor this module
replaces: the non-subsection site root's content skips apply_text_fixups
entirely (see scripts/tests/test_tree.py's module docstring for the trace).

One behavior is deliberately NOT preserved: ContentProcessor's weight
formula only correctly ordered a heading's siblings by their true source
position for the top two heading levels; anything deeper silently collapsed
to a constant weight (main content) or the parent's own weight
(sub-sections). This produced a real, confirmed-in-the-rendered-site bug --
Hugo's sidebar tie-breaks equal weights alphabetically, scrambling the
reading order of every sub-section and the deeper parts of the main guide.
parse_tree instead weights every non-root page by its true 1-based position
among its actual parent's children, at every depth -- trivial here since,
unlike ContentProcessor.structure, this module's tree nests every heading
level correctly to begin with.
"""
import io
import os
import re
from dataclasses import dataclass, field, replace
from typing import Iterator, List

from .utils import clean_source_content, extract_heading_text, get_heading_level, github_anchor
from .crossref import CrossReferenceConverter


@dataclass
class Page:
    title: str
    content: str
    raw_content: str
    path_parts: List[str]
    level: int
    line: int
    weight: int
    children: List['Page'] = field(default_factory=list)

    @property
    def has_children(self) -> bool:
        return len(self.children) > 0


def walk(root: Page) -> Iterator[Page]:
    """Pre-order walk of a page and all its descendants."""
    yield root
    for child in root.children:
        yield from walk(child)


def parse_tree(
    markdown_text: str,
    is_subsection: bool = False,
    base_line: int = 1,
    subsection_index: int = 0,
) -> Page:
    """
    Parse markdown text into a Page tree.

    Assumes (as every real Clean ABAP source file does) the text starts with
    exactly one level-1 heading, which becomes the returned root page -- its
    own path_parts is always [] (the root is never part of the output URL).
    Every subsequent heading nests under its true parent, regardless of
    heading level, so a tree-walking writer can reach and write all of them.
    """
    lines = clean_source_content(io.StringIO(markdown_text).readlines())

    root: Page = None
    stack: List[Page] = []
    content_buffer: List[str] = []

    def flush() -> None:
        if content_buffer and stack:
            text = ''.join(content_buffer).strip()
            stack[-1].content = text
            stack[-1].raw_content = text
        content_buffer.clear()

    for i, line in enumerate(lines):
        line_num = base_line + i + 1
        heading_level = get_heading_level(line)

        if heading_level is None:
            content_buffer.append(line)
            continue

        flush()

        heading_text = extract_heading_text(line)
        if not heading_text:
            continue

        while stack and stack[-1].level >= heading_level:
            stack.pop()

        folder_name = github_anchor(heading_text)
        path_parts = stack[-1].path_parts + [folder_name] if stack else []

        page = Page(
            title=heading_text,
            content='',
            raw_content='',
            path_parts=path_parts,
            level=heading_level,
            line=line_num,
            weight=0,
        )

        if not stack:
            page.path_parts = []
            page.weight = 1 if not is_subsection else (subsection_index + 1) * 10
            root = page
        else:
            parent = stack[-1]
            page.weight = (len(parent.children) + 1) * 10
            parent.children.append(page)

        stack.append(page)

    flush()
    return root


def resolve_links(root: Page, converter: CrossReferenceConverter) -> Page:
    """Rewrite cross-reference links in every page's content. Returns a new tree."""
    return replace(
        root,
        content=converter.convert_content(root.content),
        children=[resolve_links(child, converter) for child in root.children],
    )


_IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')


def _fix_image_references(content: str) -> str:
    def fix(match: 're.Match') -> str:
        alt_text, image_path = match.group(1), match.group(2)
        if image_path.startswith('http://') or image_path.startswith('https://') or image_path.startswith('/'):
            return match.group(0)
        return f"![{alt_text}]({os.path.basename(image_path)})"

    return _IMAGE_PATTERN.sub(fix, content)


def _fix_below_references(content: str) -> str:
    content = re.sub(r'\b(suggestions)\s+below\b', r'\1 on this site', content, flags=re.IGNORECASE)
    content = re.sub(r'\b(recommendations)\s+below\b', r'\1 on this site', content, flags=re.IGNORECASE)
    content = re.sub(r'\b(detailed\s+)?rules\s+below\b', r'related rules', content, flags=re.IGNORECASE)
    return content


_SHORTHAND_LONGHAND_TABLE_PATTERN = re.compile(
    r'^Shorthand\s*\|\s*Longhand\s*\|?[ \t]*\n'
    r'-+\s*\|\s*-+\s*\|?[ \t]*\n'
    r'((?:.*\|.*\n?)+)',
    re.MULTILINE,
)


def _fix_shorthand_longhand_tables(content: str) -> str:
    """
    Rewrite a "Shorthand | Longhand" source table into a fenced ABAP code block
    with a trailing " short/long comment on each line -- easier to compare and
    enables syntax highlighting.
    """
    def unescape(cell: str) -> str:
        return cell.strip().replace('\\`', '`')

    def fix(match: 're.Match') -> str:
        lines = []
        for row in match.group(1).strip('\n').split('\n'):
            short, long_form = (unescape(cell) for cell in row.strip().strip('|').split('|'))
            lines.append(f'{short} " short')
            lines.append(f'{long_form} " long')
            lines.append('')
        body = '\n'.join(lines).rstrip('\n')
        return f"```ABAP\n{body}\n```"

    return _SHORTHAND_LONGHAND_TABLE_PATTERN.sub(fix, content)


def _flatten_field(root: Page, field: str) -> str:
    parts = []
    for page in walk(root):
        value = getattr(page, field)
        if page is root:
            if value:
                parts.append(value)
            continue
        heading = f"{'#' * page.level} {page.title}"
        parts.append(f"{heading}\n\n{value}" if value else heading)
    return '\n\n'.join(parts)


def flatten_to_single_page(root: Page) -> Page:
    """
    Collapse an entire sub-section tree into one leaf Page, reconstructing
    every descendant heading as literal markdown ('#' * level) in original
    document order (walk() already yields exactly that order -- see its
    docstring). Used for dives configured to render as one page instead of
    being split per heading (see data/mapping.toml's [files].keep).

    content and raw_content are flattened independently since they can
    diverge after apply_text_fixups (which rewrites .content's image paths
    to a bare filename but leaves .raw_content as the original source text
    that _copy_images_for_content needs to find the file on disk).
    """
    return replace(
        root,
        content=_flatten_field(root, 'content'),
        raw_content=_flatten_field(root, 'raw_content'),
        children=[],
    )


def apply_text_fixups(root: Page, is_subsection: bool = False) -> Page:
    """
    Rewrite image references (to a bare filename) and stale "below"
    references in every page's content. Returns a new tree.

    The non-subsection site root is exempt -- ContentProcessor generated it
    via a separate code path that never applied either fixup, only
    cross-reference conversion (see resolve_links).
    """
    def fix(page: Page, is_root: bool) -> Page:
        content = page.content
        if not is_root:
            content = _fix_image_references(content)
            content = _fix_below_references(content)
            content = _fix_shorthand_longhand_tables(content)
        return replace(
            page,
            content=content,
            children=[fix(child, False) for child in page.children],
        )

    return fix(root, not is_subsection)
