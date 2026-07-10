---
title: "Don't chain assignments"
weight: 210
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-chain-assignments"
---

```abap
" anti-pattern
var1 = var2 = var3.
```

Chained assignments usually confuse the reader. Besides, the inline declaration doesn't work in any position of a multiple assignment.

```abap
var2 = var3.
var1 = var3.
```

Furthermore, the anti-pattern looks ambiguous because `=` is used for comparisons and assignments in ABAP. It looks similar to how other programming languages implement comparisons, for example `a = ( b == c )` in JavaScript. [Use `xsdbool` for comparisons.](/clean-code/booleans/use-xsdbool-to-set-boolean-variables/)
