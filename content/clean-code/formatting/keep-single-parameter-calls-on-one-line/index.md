---
title: "Keep single parameter calls on one line"
weight: 120
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#keep-single-parameter-calls-on-one-line"
---

```ABAP
DATA(unique_list) = remove_duplicates( list ).
remove_duplicates( CHANGING list = list ).
```

instead of the needlessly longer

```ABAP
" anti-pattern
DATA(unique_list) = remove_duplicates(
                           list ).
DATA(unique_list) = remove_duplicates(
                         CHANGING
                           list = list ).
```
