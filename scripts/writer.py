"""
Thin Hugo-writing adapter. Walks an already parsed/resolved/fixed-up Page
tree (see scripts/tree.py) and does the actual disk I/O: writing content
files and copying referenced images. Knows nothing about markdown parsing,
cross-reference resolution, or text fixups.

The non-subsection site root is a special case, mirroring the old
ContentProcessor._generate_root_file: hardcoded weight 1, a different
source-URL function, written straight to base_path/_index.md. Every other
page -- including a sub-section's own root heading -- goes through the same
normal per-page write path.
"""
import os
import re
import shutil

from .tree import Page
from .frontmatter import generate_front_matter, get_root_source_url, get_source_url
from .utils import ensure_directory

_IMAGE_REF_PATTERN = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.svg')


def write_tree(root: Page, base_path: str, source_file: str, is_subsection: bool = False) -> int:
    """
    Write a page tree's content to disk. Returns the number of files written.
    """
    if not is_subsection:
        count = _write_root_page(root, base_path)
        for child in root.children:
            count += _write_page(child, base_path, source_file, is_subsection)
        return count

    return _write_page(root, base_path, source_file, is_subsection)


def _write_root_page(root: Page, base_path: str) -> int:
    front_matter = generate_front_matter(title=root.title, weight=1, source=get_root_source_url())
    content = front_matter
    if root.content:
        content += f"\n{root.content}\n"

    ensure_directory(base_path)
    with open(os.path.join(base_path, '_index.md'), 'w', encoding='utf-8') as f:
        f.write(content)
    return 1


def _write_page(page: Page, base_path: str, source_file: str, is_subsection: bool) -> int:
    folder_path = os.path.join(base_path, *page.path_parts)

    source_url = get_source_url(source_file, is_subsection=is_subsection, heading_text=page.title)
    front_matter = generate_front_matter(title=page.title, weight=page.weight, source=source_url)
    content = front_matter
    if page.content:
        content += f"\n{page.content}\n"

    filename = '_index.md' if page.has_children else 'index.md'
    ensure_directory(folder_path)
    with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as f:
        f.write(content)

    _copy_images_for_content(folder_path, page.raw_content, source_file, is_subsection)

    count = 1
    for child in page.children:
        count += _write_page(child, base_path, source_file, is_subsection)
    return count


def _copy_images_for_content(target_folder: str, content: str, source_file: str, is_subsection: bool) -> None:
    # Only sub-sections have image directories alongside their source file.
    if not is_subsection:
        return

    source_dir = os.path.dirname(source_file)

    for image_path in _IMAGE_REF_PATTERN.findall(content):
        filename = os.path.basename(image_path)

        if not any(filename.lower().endswith(ext) for ext in _IMAGE_EXTENSIONS):
            continue
        if filename.endswith('.vsdx'):
            continue

        source_path = None
        full_source_path = os.path.join(source_dir, image_path)
        if os.path.exists(full_source_path):
            source_path = full_source_path
        else:
            test_source_path = os.path.join(source_dir, filename)
            if os.path.exists(test_source_path):
                source_path = test_source_path
            else:
                for root_dir, _dirs, files in os.walk(source_dir):
                    if filename in files:
                        source_path = os.path.join(root_dir, filename)
                        break

        if source_path and os.path.exists(source_path):
            ensure_directory(target_folder)
            shutil.copy2(source_path, os.path.join(target_folder, filename))
