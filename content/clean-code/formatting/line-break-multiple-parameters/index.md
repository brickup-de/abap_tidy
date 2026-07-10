---
title: "Line-break multiple parameters"
weight: 150
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#line-break-multiple-parameters"
---

```ABAP
DATA(sum) = add_two_numbers( value_1 = 5
                             value_2 = 6 ).
```

Yes, this wastes space.
However, otherwise, it's hard to spot where one parameter ends and the next starts:

```ABAP
" anti-pattern
DATA(sum) = add_two_numbers( value_1 = 5 value_2 = 6 ).
```
