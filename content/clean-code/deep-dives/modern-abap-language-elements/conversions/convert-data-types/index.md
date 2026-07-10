---
title: "Convert data types"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#convert-data-types"
---

Use the operator `CONV #( )` to convert data types and save temporary variables.

```ABAP
method_takes_string( CONV #( a_char ) ).
```

Old style:

```ABAP
DATA a_string TYPE string.
a_string = a_char.
method_takes_string( a_string ).
```
