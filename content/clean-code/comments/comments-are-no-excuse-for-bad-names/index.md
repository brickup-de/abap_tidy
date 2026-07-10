---
title: "Comments are no excuse for bad names"
weight: 20
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#comments-are-no-excuse-for-bad-names"
---

```ABAP
DATA(input_has_entries) = has_entries( input ).
```

Improve your names instead of explaining what they really mean or why you chose bad ones.

```ABAP
" anti-pattern
" checks whether the table input contains entries
DATA(result) = check_table( input ).
```
