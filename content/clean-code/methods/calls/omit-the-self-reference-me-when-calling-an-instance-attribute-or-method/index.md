---
title: "Omit the self-reference me when calling an instance attribute or method"
linkTitle: "Omit the self-reference me"
weight: 70
params:
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
