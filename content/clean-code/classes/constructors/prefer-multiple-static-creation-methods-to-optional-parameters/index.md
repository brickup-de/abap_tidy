---
title: "Prefer multiple static creation methods to optional parameters"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-multiple-static-creation-methods-to-optional-parameters"
---

```ABAP
CLASS-METHODS describe_by_data IMPORTING data TYPE any [...]
CLASS-METHODS describe_by_name IMPORTING name TYPE any [...]
CLASS-METHODS describe_by_object_ref IMPORTING object_ref TYPE REF TO object [...]
CLASS-METHODS describe_by_data_ref IMPORTING data_ref TYPE REF TO data [...]
```

ABAP does not support [overloading](https://en.wikipedia.org/wiki/Function_overloading).
Use name variations and not optional parameters to achieve the desired semantics.

```ABAP
" anti-pattern
METHODS constructor
  IMPORTING
    data       TYPE any OPTIONAL
    name       TYPE any OPTIONAL
    object_ref TYPE REF TO object OPTIONAL
    data_ref   TYPE REF TO data OPTIONAL
  [...]
```

The general guideline
[_Split methods instead of adding OPTIONAL parameters_](/clean-code/methods/parameter-number/split-methods-instead-of-adding-optional-parameters/)
explains the reasoning behind this.

Consider resolving complex constructions to a multi-step construction with the
[Builder design pattern](https://en.wikipedia.org/wiki/Builder_pattern).
