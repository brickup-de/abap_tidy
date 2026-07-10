---
title: "Lower and upper case conversion"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#lower-and-upper-case-conversion"
---

Convert characters between cases using `to_upper( )` or `to_lower( )`.

```ABAP
DATA(uppercase) = to_upper( lowercase ).
DATA(lowercase) = to_lower( uppercase ).
```

Old style:

```ABAP
TRANSLATE lowercase TO UPPER CASE.
```
