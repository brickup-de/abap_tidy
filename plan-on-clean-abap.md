# Plan: Convert Clean ABAP to Hugo Content Structure

## Overview

Split `CleanABAP.md` and the `sub-sections/` folder into individual Hugo content pages, preserving the heading hierarchy as folder hierarchy. Cross-references must work in the generated Hugo site.

## Source Material

- Primary: `./assets/sources/sap-styleguides/clean-abap/CleanABAP.md`
- Secondary: `./assets/sources/sap-styleguides/clean-abap/sub-sections/` (7 markdown files)
- Language: English only (ignore other language versions)
- Ignore: `cheat-sheet/` folder and its contents

## Output Location

All generated content goes into `./content/clean-code/` in the Hugo project.

## Folder and File Structure

### Principle
Each heading level (##, ###, ####, etc.) becomes its own folder with an `_index.md` file. The folder name is the kebab-case version of the heading text.

### Root Structure
```
content/clean-code/
├── _index.md                    # Intro page, weight 1
├── how-to/
│   └── _index.md                # ## How to, weight 10
│   ├── get-started-with-clean-code/
│   │   └── _index.md            # ### How to Get Started..., weight 10
│   ├── refactor-legacy-code/
│   │   └── _index.md            # ### How to Refactor..., weight 20
│   └── ...
├── names/
│   └── _index.md                # ## Names, weight 20
│   ├── use-descriptive-names/
│   │   └── _index.md            # ### Use descriptive names, weight 10
│   └── ...
├── ...
└── deep-dives/
    └── _index.md                # Deep Dives landing, weight 10
    ├── interfaces-vs-abstract-classes/
    │   └── _index.md            # From InterfacesVsAbstractClasses.md, weight 10
    │   ├── interfaces/
    │   │   └── _index.md        # ## Interfaces, weight 10
    │   └── ...
    └── ...
```

### Deep Dives Section
- All content from `sub-sections/` folder goes under `content/clean-code/deep-dives/`
- `deep-dives/_index.md` contains: "Deep dive articles on specific topics from the Clean ABAP styleguide."
- Each sub-section markdown file becomes a folder under `deep-dives/`
- Sub-section files are also split by their heading hierarchy

## Weight Scheme

Each page's weight = (its 1-based position among its siblings) × 10

**Examples:**
- `content/clean-code/_index.md`: weight 1 (special case - 0 goes to end in Hugo)
- First `##` chapter: weight 10
- Second `##` chapter: weight 20
- First `###` under a parent: weight 10
- Second `###` under same parent: weight 20
- `deep-dives/_index.md`: weight 190 (19th sibling in clean-code/)
- First deep-dives sub-section: weight 20 (2nd child in deep-dives/)
- Second deep-dives sub-section: weight 30

## Kebab-Case Transformation

Convert heading text to folder names using:
- Lowercase all characters
- Replace spaces with hyphens
- Remove all punctuation (commas, periods, apostrophes, parentheses, etc.)

**Examples:**
- "How to" → `how-to`
- "Get Started with Clean Code" → `get-started-with-clean-code`
- "Avoid encodings, esp. Hungarian notation" → `avoid-encodings-esp-hungarian-notation`
- "Use descriptive names" → `use-descriptive-names`
- "Interfaces vs. Abstract Classes" → `interfaces-vs-abstract-classes`

## Content Processing

### What to Remove

1. **Language navigation block** (lines 3-17):
   ```markdown
   > [**English**](CleanABAP.md)
   > &nbsp;·&nbsp;
   > [中文](CleanABAP_zh.md)
   > ...
   ```

2. **Breadcrumb navigation lines**: All lines matching pattern `> [Clean ABAP](#clean-abap) > [Content](#content) > ...`

3. **Cheat Sheet link**: The sentence "The [Cheat Sheet](cheat-sheet/CheatSheet.md) is a print-optimized version."

4. **TOC section**: The entire `## Content` section (lines 27-254, or until `## How to`)

### What to Keep

- Title "# Clean ABAP" → goes into front matter title of `content/clean-code/_index.md`
- Intro text: "This guide is an adoption of Robert C. Martin's _Clean Code_ for [ABAP](https://en.wikipedia.org/wiki/ABAP)." → goes into `content/clean-code/_index.md` content
- All chapter content, body text, lists, code examples, etc.

### Special Content

- `deep-dives/_index.md` content: "Deep dive articles on specific topics from the Clean ABAP styleguide."

## Front Matter

Every `_index.md` file must have front matter with these fields:

```yaml
---
title: "Heading Text"
weight: 10  # position among siblings × 10
date: 2026-07-05  # optional, for consistency
license: "CC BY 3.0"
license_url: "https://creativecommons.org/licenses/by/3.0/"
source: "https://github.com/SAP/styleguides/blob/main/clean-abap/[path]#L[line]"
---
```

### Source URL Rules

- For pages from `CleanABAP.md`: `https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#L[line]`
- For pages from sub-sections: `https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/[filename].md#L[line]`
- For synthetic pages:
  - `content/clean-code/_index.md`: `https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#L1`
  - `content/clean-code/deep-dives/_index.md`: `https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/`

## Cross-References

Convert all markdown anchor links to absolute path links:

**Format:** `[link text](/clean-code/path/to/page/)`

**Rules:**
- Preserve the original link text
- Path is absolute from site root
- Convert heading anchors to folder paths (using kebab-case)
- Hugo's embedded render hook automatically resolves these to correct relative URLs

**Examples:**
- `[How to](#how-to)` → `[How to](/clean-code/how-to/)`
- `[Use descriptive names](#use-descriptive-names)` → `[Use descriptive names](/clean-code/names/use-descriptive-names/)`
- `[custom text](#some-anchor)` → `[custom text](/clean-code/path/to/anchor/page)`

**Note:** Since each heading becomes its own page, the anchor part of the URL maps directly to the page path.

## Image Handling

### Source Images
- Only `sub-sections/interfaces-vs-abstract-classes/` contains images (3 PNG files)
- Images: `InterfacesVsAbstractClasses-Interface.png`, `InterfacesVsAbstractClasses-AbstractClass.png`, `InterfacesVsAbstractClasses-Combined.png`
- Ignore `.vsdx` file (Visio source)

### Processing
1. Copy PNG files to the same folder as the `_index.md` that references them
2. Update image references in markdown:
   - From: `![](interfaces-vs-abstract-classes/InterfacesVsAbstractClasses-Interface.png)`
   - To: `![](InterfacesVsAbstractClasses-Interface.png)`

### Hugo Integration
- Use Hugo page resources (bundle images with content)
- Images are placed in the same directory as the `_index.md` file
- References use relative paths

## Sub-Sections Processing

The 7 files in `sub-sections/` are:
1. `AvoidEncodings.md`
2. `Enumerations.md`
3. `Exceptions.md`
4. `FunctionGroupsVsClasses.md`
5. `InterfacesVsAbstractClasses.md` (has images)
6. `ModernABAPLanguageElements.md`
7. `UpperVsLowerCase.md`

**Rules:**
- Apply the same splitting logic as CleanABAP.md
- Each file's `#` heading becomes a folder under `deep-dives/`
- Filename kebab-case matches heading kebab-case for all files
- Process all heading levels within each file
- Copy associated images (only for InterfacesVsAbstractClasses.md)

## Implementation Notes

### Parsing Strategy
- Read markdown files line by line
- Track heading hierarchy using a stack
- Extract content between headings
- Maintain current path based on heading level

### Path Construction
- `#` heading → ignored (title only, goes to parent's _index.md front matter)
- `##` heading → folder at root of clean-code/ or deep-dives/
- `###` heading → subfolder under parent `##`
- `####` heading → subfolder under parent `###`
- etc.

### Weight Calculation
- For each parent folder, count children
- Assign weight = (child_index + 1) × 10
- Child index is 1-based position in parent

### Special Cases
- `content/clean-code/_index.md`: weight 1 (not 0, as 0 sorts to end in Hugo)
- `content/clean-code/deep-dives/_index.md`: weight 190 (after 18 Clean ABAP chapters at 10-180)

## Verification

After generation, verify:
1. All content from original files is present
2. No removed content (language nav, breadcrumbs, TOC, cheat sheet link) remains
3. All cross-references use `relref` shortcode
4. All image references use relative paths
5. Folder structure matches heading hierarchy
6. Weights produce correct reading order
7. Front matter is complete on all pages
8. Hugo build succeeds without errors
