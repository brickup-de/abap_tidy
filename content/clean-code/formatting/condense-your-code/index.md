---
title: "Condense your code"
weight: 70
params:
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
