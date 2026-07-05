# URL Mapping and Redirect Implementation Tasks

This document tracks the implementation tasks for the URL control system. Nothing below is implemented yet.

## Overview

Implement a system that allows customizing and simplifying generated URLs while maintaining URL stability through redirects and warnings.

## Tasks

### 1. Create URL Configuration System

- [ ] Create `scripts/urls.py` module
- [ ] Implement config file loading from `data/mapping/{base-path}.yaml`
- [ ] Derive base path from config filename (e.g., `clean-code.yaml` → `/clean-code/`)
- [ ] Parse hierarchical YAML config into internal data structure

### 2. Config Synchronization

- [ ] Implement content tree extraction from generated structure
- [ ] Implement full config sync: regenerate complete tree from content
- [ ] Preserve all `__`-prefixed entries (`__rename`, `__aliases`) during sync
- [ ] Add non-`__` structural entries for all pages without customizations
- [ ] Write synced config back to YAML file (maintain formatting)

### 3. URL Transformation

- [ ] Implement `__rename` application for any path segment (directory or leaf)
- [ ] Ensure parent `__rename` propagates to all children
- [ ] Generate transformed path for each heading based on config
- [ ] Fall back to default kebab-case for path segments without `__rename`

### 4. Path Mapping Integration

- [ ] Modify `main.py` to load and sync config before content generation
- [ ] Transform the heading-to-path mapping using config directives
- [ ] Pass transformed mapping to `CrossReferenceConverter` in `crossref.py`
- [ ] Ensure all cross-references use transformed URLs

### 5. Alias/Redirect Support

- [ ] Extract `__aliases` from config for each page
- [ ] Add `aliases` field to Hugo front matter for pages with `__aliases`
- [ ] Ensure aliases are absolute URLs
- [ ] Verify Hugo generates correct redirect files on build

### 6. Published URLs Tracking

- [ ] Create/update `data/published_urls.txt` management
- [ ] Append newly generated URLs during content generation
- [ ] Maintain alphabetical sort order (not just append at end)
- [ ] Deduplicate entries

### 7. URL Change Detection and Warnings

- [ ] Collect all generated URLs after transformation
- [ ] Compare against `data/published_urls.txt`
- [ ] Detect new URLs (not in published list)
- [ ] Detect changed URLs (exist in published but different)
- [ ] Print warnings to console with concrete differences

### 8. First-Run Handling

- [ ] Handle missing `data/mapping/clean-code.yaml` on first run
- [ ] Handle missing `data/published_urls.txt` on first run
- [ ] Generate initial config from content tree (no `__` directives)
- [ ] Generate initial published URLs from first generation

### 9. Testing

- [ ] Test URL transformation with various config scenarios
- [ ] Test `__rename` propagation to children
- [ ] Test `__aliases` generate correct Hugo front matter
- [ ] Test published URLs tracking and sorting
- [ ] Test URL change detection warnings
- [ ] Test cross-references use transformed URLs
- [ ] Test redirects work on deployed site

### 10. Documentation

- [ ] Update this document with implementation notes as tasks are completed
- [ ] Add examples of common URL customization patterns
- [ ] Document any edge cases or limitations

## Configuration Format

URL customizations will be defined in YAML files under `data/mapping/`. Example:

```yaml
# data/mapping/clean-code.yaml
methods:
  methods-object-orientation:
    __rename: object-orientation
    __aliases:
      - /clean-code/old-methods-path/
    prefer-instance-to-static-methods:
      __rename: prefer-instance-to-static

classes:
  classes-object-orientation:
    __rename: object-orientation
```

**Directives:**
- `__rename`: Rename this path segment (applies to directories and leaf pages)
- `__aliases`: List of absolute URLs to redirect to this page

## Expected Behavior

1. Config file is complete - includes all pages, not just customized ones
2. Non-`__` entries are structural placeholders with default kebab-case URLs
3. `__` prefixed entries are preserved during config sync
4. Published URLs file is always sorted alphabetically
5. Aliases move with the page if the page's URL changes later
6. All crosslinks continue to work with transformed URLs

## File Locations

| File | Purpose |
|------|---------|
| `data/mapping/clean-code.yaml` | URL customization config |
| `data/published_urls.txt` | All ever-published URLs |
| `scripts/urls.py` | Implementation module (to be created) |
| `scripts/main.py` | Integration point (to be modified) |
| `scripts/crossref.py` | Uses transformed path mapping (to be modified) |
