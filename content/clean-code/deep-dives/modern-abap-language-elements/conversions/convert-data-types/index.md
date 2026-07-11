---
title: "Convert data types"
weight: 10
params:
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
