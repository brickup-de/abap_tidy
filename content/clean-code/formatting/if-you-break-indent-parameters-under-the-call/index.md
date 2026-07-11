---
title: "If you break, indent parameters under the call"
weight: 140
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#if-you-break-indent-parameters-under-the-call"
---

```ABAP
DATA(sum) = add_two_numbers(
                value_1 = 5
                value_2 = 6 ).
```

Aligning the parameters elsewhere makes it hard to spot what they belong to:

```ABAP
" anti-pattern
DATA(sum) = add_two_numbers(
    value_1 = 5
    value_2 = 6 ).
```

However, this is the best pattern if you want to avoid the formatting to be broken by a name length change.
