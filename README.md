# abap_tidy

A Hugo site that turns SAP's [Clean ABAP](https://github.com/SAP/styleguides) style guide into a browsable, cross-referenced docs site, built on the [Hextra](https://github.com/imfing/hextra) theme.

The Markdown under `content/clean-code/` is **generated**, not hand-written — it's produced from the upstream style guide by a Python conversion pipeline (`scripts/`), so headings, internal links, and cross-references stay in sync with the source instead of drifting out of date.

## Quick start

```sh
git submodule update --init --recursive   # pull in the source style guides
npm install
npm run dev                               # hugo server at localhost:1313 (no ABAP syntax highlighting)
```

Other scripts:

```sh
npm run build     # hugo --minify + ABAP syntax highlighting pass
npm run preview   # build, then serve /public on :1414 (with syntax highlighting)
```

## How content is generated

`assets/sources/` holds the upstream style guides as git submodules:

| Submodule | Wired into the site? |
|---|---|
| `sap-styleguides` (SAP/styleguides) | Yes — source for `content/clean-code/` |
| `sap-abap-cheat-sheets` | Not yet |
| `dsag-abap-leitfaden` | Not yet |

`refresh_content.py` runs the conversion pipeline in `scripts/` (`main.py`, `tree.py`, `crossref.py`, `frontmatter.py`, `writer.py`) to turn `assets/sources/sap-styleguides/clean-abap/` into the Hugo pages under `content/clean-code/`.

```sh
python3 refresh_content.py
```

**No hand-edited files under `content/`** — they're regenerated output and are versioned so diffs are easy to review. To change the generated content, change the script and re-run it.

## Tests

```sh
python3 -m pytest scripts/tests/
```

## Repo layout

- `scripts/` — the Markdown → Hugo conversion pipeline and its tests
- `content/` — generated Hugo content (do not edit directly)
- `assets/sources/` — upstream style guides, as git submodules
- `layouts/` — Hugo template overrides (Hextra theme customizations)
- `docs/agents/` — process docs for AI coding agents working in this repo (issue tracking, triage labels, domain docs)

See [AGENTS.md](AGENTS.md) for the ground rules agents should follow when working in this repo.
