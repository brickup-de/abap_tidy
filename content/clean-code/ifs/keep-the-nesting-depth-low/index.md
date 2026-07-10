---
title: "Keep the nesting depth low"
weight: 30
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#keep-the-nesting-depth-low"
---

```ABAP
" anti-pattern
IF <this>.
  IF <that>.
  ENDIF.
ELSE.
  IF <other>.
  ELSE.
    IF <something>.
    ENDIF.
  ENDIF.
ENDIF.
```

Nested `IF`s get hard to understand very quickly and require an exponential number of test cases for complete coverage.

Decision trees can usually be taken apart by forming sub-methods and introducing boolean helper variables.

Other cases can be simplified by merging IFs, such as

```ABAP
IF <this> AND <that>.
```

instead of the needlessly nested

```ABAP
" anti-pattern
IF <this>.
  IF <that>.
```
