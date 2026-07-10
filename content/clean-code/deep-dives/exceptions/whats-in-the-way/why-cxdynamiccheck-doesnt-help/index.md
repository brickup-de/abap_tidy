---
title: "Why CX_DYNAMIC_CHECK Doesn't Help"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#why-cxdynamiccheck-doesnt-help"
---

`cx_dynamic_check` doesn't improve this.
Alhough it makes the syntax check accept the missing redeclaration
and catch block in `middle_method`,
the code will still trigger `cx_sy_no_handler`
if the exception is actually thrown.
