---
title: "Use own super classes"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-own-super-classes"
---

```ABAP
CLASS cx_fra_static_check DEFINITION ABSTRACT INHERITING FROM cx_static_check.
CLASS cx_fra_no_check DEFINITION ABSTRACT INHERITING FROM cx_no_check.
```

Consider creating abstract super classes for each exception type for your application,
instead of sub-classing the foundation classes directly.
Allows you to `CATCH` all _your_ exceptions.
Enables you to add common functionality to all exceptions, such as special text handling.
`ABSTRACT` prevents people from accidentally using these non-descriptive errors directly.
