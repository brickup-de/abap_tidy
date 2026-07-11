---
title: "Prefer LINE_EXISTS to READ TABLE or LOOP AT"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-line_exists-to-read-table-or-loop-at"
---

```ABAP
IF line_exists( my_table[ key = 'A' ] ).
```

expresses the intent clearer and shorter than

```ABAP
" anti-pattern
READ TABLE my_table TRANSPORTING NO FIELDS WITH KEY key = 'A'.
IF sy-subrc = 0.
```

or even

```ABAP
" anti-pattern
LOOP AT my_table REFERENCE INTO DATA(line) WHERE key = 'A'.
  line_exists = abap_true.
  EXIT.
ENDLOOP.
```
