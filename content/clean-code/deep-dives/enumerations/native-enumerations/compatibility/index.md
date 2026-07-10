---
title: "Compatibility"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#compatibility"
---

To integrate native enumerations with legacy code that uses constants the `BASE TYPE` addition is available:
```ABAP
CLASS /compatbl/message_severity DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    TYPES: BEGIN OF ENUM type BASE TYPE symsgty,
            info      VALUE 'I',
            exit      VALUE 'X',
            undefined VALUE IS INITIAL,
          END OF ENUM type.
```
This allows a conversion from and to enumerated variables using the `CONV` operator.
```ABAP
"yields 'I'
DATA(severity_as_char) = CONV symsgty( /compatbl/message_severity=>info ). 

"yields /compatbl/message_severity=>exit
DATA(severity) = CONV /compatbl/message_severity=>type( 'X' ). 
```

The conversion operator is mandatory to satisfy the strict type check.
It needs to be incorporated at all places where APIs with legacy types are operated or whenever data is queried or persisted with ABAP SQL.

For example, if the method signature of `log_contains` with a single `IMPORTING` parameter typed as `symsgty` cannot be refactored it will have to be called like this:
```ABAP
IF log_contains( CONV #( /compatbl/message_severity=>warning ) ).
```
