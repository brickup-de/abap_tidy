---
title: "Don't clear VALUE parameters"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-clear-value-parameters"
---

Parameters that work by `VALUE` are handed over as new, separate memory areas that are empty by definition.
Don't clear them again:

```ABAP
METHODS square
  EXPORTING
    VALUE(result) TYPE i.

METHOD square.
  " no need to CLEAR result
ENDMETHOD.
```

`RETURNING` parameters are always `VALUE` parameters, so you never have to clear them:

```ABAP
METHODS square
  RETURNING
    VALUE(result) TYPE i.

METHOD square.
  " no need to CLEAR result
ENDMETHOD.
```
