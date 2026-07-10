---
title: "Condense your code"
weight: 70
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#condense-your-code"
---

```ABAP
DATA(result) = calculate( items ).
```

instead of adding unneeded blanks

```ABAP
" anti-pattern
DATA(result)        =      calculate(    items =   items )   .
```
