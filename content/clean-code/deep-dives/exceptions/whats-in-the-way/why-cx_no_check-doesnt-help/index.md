---
title: "Why CX_NO_CHECK Doesn't Help"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#why-cx_no_check-doesnt-help"
---

`cx_no_check` also doesn't help.
Although it makes the method bodies work,
the `METHODS lower_method` definition now is
no longer allowed to declare `/clean/flexible_exception`
and compilation fails with a syntax error.
