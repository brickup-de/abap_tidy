# Clean ABAP to Hugo Conversion Scripts

This directory contains Python scripts for converting the Clean ABAP markdown content into a Hugo-compatible content structure.

## Overview

The scripts process the Clean ABAP markdown files and generate a folder hierarchy where each heading level becomes a folder with an `_index.md` file. This structure is compatible with Hugo's content organization and allows for proper navigation and cross-referencing.

## File Structure

- `utils.py` - Utility functions (kebab-case conversion, content cleaning, etc.)
- `frontmatter.py` - Front matter generation for Hugo content
- `crossref.py` - Cross-reference conversion logic
- `processor.py` - Main content processing logic
- `main.py` - Main execution script
- `__init__.py` - Package initialization

## Usage

### Run the Conversion

From the repository root, run:

```bash
python3 run_conversion.py
```

Or from the scripts directory:

```bash
cd scripts
python3 main.py
```

### Configuration

The script automatically:
- Reads from `assets/sources/sap-styleguides/clean-abap/CleanABAP.md`
- Processes all `.md` files in `assets/sources/sap-styleguides/clean-abap/sub-sections/`
- Outputs to `content/clean-code/`

## Features

### Content Processing
- Removes language navigation blocks
- Removes breadcrumb navigation lines
- Removes TOC section
- Removes cheat sheet links
- Preserves all other content including code examples, lists, etc.

### Folder Structure
- Each heading level (##, ###, ####, etc.) becomes a folder with `_index.md`
- Folder names use kebab-case transformation
- Maintains the heading hierarchy as folder hierarchy

### Front Matter
- Generates proper Hugo front matter with:
  - Title from heading text
  - Weight based on position among siblings
  - Source URL pointing to original GitHub location
  - License information (CC BY 3.0)
  - Date (2026-07-05)

### Cross-References
- Converts markdown anchor links to absolute Hugo paths
- Pattern: `[link text](#anchor)` → `[link text](/clean-code/path/to/page/)`
- Handles both internal and external links
- Preserves external links (http/https)

### Sub-Sections
- Each sub-section file becomes a folder under `deep-dives/`
- Filename kebab-case matches heading kebab-case
- Folder names:
  - AvoidEncodings.md → `deep-dives/avoid-encodings/`
  - InterfacesVsAbstractClasses.md → `deep-dives/interfaces-vs-abstract-classes/`
  - etc.

### Images
- Copies PNG images from `sub-sections/interfaces-vs-abstract-classes/`
- Places images in the same folder as the `_index.md` that references them
- Updates image references to use relative paths

## Weight Scheme

- `content/clean-code/_index.md`: weight 1
- First `##` chapter: weight 10
- Second `##` chapter: weight 20
- First `###` under a parent: weight 10
- Second `##` under same parent: weight 20
- `deep-dives/_index.md`: weight 190
- First deep-dives sub-section: weight 10 (1st child in deep-dives/)
- Second deep-dives sub-section: weight 20
- etc.

## Requirements

- Python 3.x
- No external dependencies required

## Known Issues

1. **Image Handling**: Currently copies all images from `interfaces-vs-abstract-classes/` to the main sub-section folder. For better organization, images should be copied to the specific folders that reference them.

2. **Link Cleaning**: Some original content may contain links like `[Back to the guide](/clean-code/clean-abap-md/)` which need manual cleanup.

3. **Special Characters**: Some heading text with special characters may not convert perfectly to kebab-case.

## Development

To add new features or modify the conversion logic:

1. Update the relevant module (`utils.py`, `processor.py`, etc.)
2. Test with a small subset of content
3. Run the full conversion to verify

## License

The conversion scripts are provided as-is for use in converting the Clean ABAP content to Hugo format. The original content remains under its original license (CC BY 3.0).
