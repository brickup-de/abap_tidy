---
title: "Do not use field symbols for dynamic data access"
weight: 40
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#do-not-use-field-symbols-for-dynamic-data-access"
---

Starting in ABAP Platform 2021, there are almost no places left where using a field symbol is necessary to perform access to generically typed variables or dynamic access to components of a variable.

So, instead of something like
```ABAP
" anti-pattern
ASSIGN dref->* TO <fs>.
result = <fs>.
```
write
```ABAP
result = dref->*.
```

Refer to [New kinds of ABAP expressions (SAP blog)](https://blogs.sap.com/2021/10/19/new-kinds-of-abap-expressions/) for more examples and detailed explanations of replacing dynamic and generic accesses via field symbols with more modern syntactical constructions.
