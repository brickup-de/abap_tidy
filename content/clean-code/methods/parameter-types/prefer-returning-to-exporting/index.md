---
title: "Prefer RETURNING to EXPORTING"
linkTitle: "Prefer RETURNING"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-returning-to-exporting"
---

```ABAP
METHODS square
  IMPORTING
    number        TYPE i
  RETURNING
    VALUE(result) TYPE i.

DATA(result) = square( 42 ).
```

Instead of the needlessly longer

```ABAP
" anti-pattern
METHODS square
  IMPORTING
    number TYPE i
  EXPORTING
    result TYPE i.

square(
  EXPORTING
    number = 42
  IMPORTING
    result = DATA(result) ).
```

`RETURNING` not only makes the call shorter,
it also allows method chaining and prevents [same-input-and-output errors](/clean-code/methods/parameter-initialization/clear-or-overwrite-exporting-reference-parameters/take-care-if-input-and-output-could-be-the-same/).
