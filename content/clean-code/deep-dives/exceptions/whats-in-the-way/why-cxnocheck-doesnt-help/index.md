---
title: "Why CX_NO_CHECK Doesn't Help"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#why-cxnocheck-doesnt-help"
---

`cx_no_check` also doesn't help.
Although it makes the method bodies work,
the `METHODS lower_method` definition now is
no longer allowed to declare `/clean/flexible_exception`
and compilation fails with a syntax error.
