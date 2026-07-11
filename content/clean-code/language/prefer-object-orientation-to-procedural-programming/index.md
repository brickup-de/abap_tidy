---
title: "Prefer object orientation to procedural programming"
weight: 30
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-object-orientation-to-procedural-programming"
---

Object-oriented programs (classes, interfaces) are segmented better
and can be refactored and tested more easily than procedural code (functions, programs).
Although there are situations where you must provide procedural objects
(a function for an RFC, a program for a transaction),
these objects should do little more than call a corresponding class that provides the actual feature:

```ABAP
FUNCTION check_business_partner [...].
  DATA(validator) = NEW /clean/biz_partner_validator( ).
  result = validator->validate( business_partners ).
ENDFUNCTION.
```

> [Function Groups vs. Classes](/clean-code/deep-dives/function-groups-vs-classes/)
> describes the differences in detail.
