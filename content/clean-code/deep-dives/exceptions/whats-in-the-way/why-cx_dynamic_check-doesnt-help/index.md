---
title: "Why CX_DYNAMIC_CHECK Doesn't Help"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#why-cx_dynamic_check-doesnt-help"
---

`cx_dynamic_check` doesn't improve this.
Alhough it makes the syntax check accept the missing redeclaration
and catch block in `middle_method`,
the code will still trigger `cx_sy_no_handler`
if the exception is actually thrown.
