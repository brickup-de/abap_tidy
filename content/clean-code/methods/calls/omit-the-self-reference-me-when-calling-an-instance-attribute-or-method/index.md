---
title: "Omit the self-reference me when calling an instance attribute or method"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#omit-the-self-reference-me-when-calling-an-instance-attribute-or-method"
---

Since the self-reference `me->` is implicitly set by the system, omit it when calling an instance attribute or method

```ABAP
DATA(sum) = aggregate_values( values ).
```

instead of the needlessly longer

```ABAP
" anti-pattern
DATA(sum) = aggregate_values( me->values ).
```

```ABAP
" anti-pattern
DATA(sum) = me->aggregate_values( values ).
```

unless there is a scope conflict between a local variable or importing parameter and an instance attribute

```ABAP
me->logger = logger.
```
