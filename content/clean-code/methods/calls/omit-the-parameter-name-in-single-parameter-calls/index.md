---
title: "Omit the parameter name in single parameter calls"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#omit-the-parameter-name-in-single-parameter-calls"
---

```ABAP
DATA(unique_list) = remove_duplicates( list ).
```

instead of the needlessly longer

```ABAP
" anti-pattern
DATA(unique_list) = remove_duplicates( list = list ).
```

There are cases, however, where the method name alone is not clear enough
and repeating the parameter name may further understandability:

```ABAP
car->drive( speed = 50 ).
update( asynchronous = abap_true ).
```
