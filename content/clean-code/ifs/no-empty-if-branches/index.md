---
title: "No empty IF branches"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#no-empty-if-branches"
---

```ABAP
IF has_entries = abap_false.
  " do some magic
ENDIF.
```

is shorter and clearer than

```ABAP
" anti-pattern
IF has_entries = abap_true.
ELSE.
  " do some magic
ENDIF.
```
