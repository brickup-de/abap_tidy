---
title: "Prefer pragmas to pseudo comments"
weight: 140
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-pragmas-to-pseudo-comments"
---

Prefer pragmas to pseudo comments to suppress irrelevant warnings and errors identified by the ATC. Pseudo comments 
have mostly become obsolete and have been replaced by pragmas.

```ABAP
" pattern
MESSAGE e001(ad) INTO DATA(message) ##NEEDED.

" anti-pattern
MESSAGE e001(ad) INTO DATA(message). "#EC NEEDED
```

Use program `ABAP_SLIN_PRAGMAS` or table `SLIN_DESC` to find the mapping between obsolete pseudo comments and the pragmas that 
have replaced them.
