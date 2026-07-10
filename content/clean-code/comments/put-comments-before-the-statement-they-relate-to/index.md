---
title: "Put comments before the statement they relate to"
weight: 70
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#put-comments-before-the-statement-they-relate-to"
---

```ABAP
" delegate pattern
output = calculate_result( input ).
```

Clearer than

```ABAP
" anti-pattern
output = calculate_result( input ).
" delegate pattern
```

And less invasive than

```ABAP
output = calculate_result( input ).  " delegate pattern
```
