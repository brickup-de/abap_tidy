---
title: "Prefer RAISE EXCEPTION NEW to RAISE EXCEPTION TYPE"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-raise-exception-new-to-raise-exception-type"
---

Note: Available from NW 7.52 onwards.

```ABAP
RAISE EXCEPTION NEW cx_generation_error( previous = exception ).
```

in general is shorter than the needlessly longer

```ABAP
RAISE EXCEPTION TYPE cx_generation_error
  EXPORTING
    previous = exception.
```

However, if you make massive use of the addition `MESSAGE`, you may want to stick with the `TYPE` variant:

```ABAP
RAISE EXCEPTION TYPE cx_generation_error
  MESSAGE e136(messages)
  EXPORTING
    previous = exception.
```
