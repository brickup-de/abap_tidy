---
title: "Prefer READ TABLE to LOOP AT"
linkTitle: "Prefer READ TABLE to LOOP"
weight: 50
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-read-table-to-loop-at"
---

```ABAP
READ TABLE my_table REFERENCE INTO DATA(line) WITH KEY key = 'A'.
```

expresses the intent clearer and shorter than

```ABAP
" anti-pattern
LOOP AT my_table REFERENCE INTO DATA(line) WHERE key = 'A'.
  EXIT.
ENDLOOP.
```

or even

```ABAP
" anti-pattern
LOOP AT my_table REFERENCE INTO DATA(line).
  IF line->key = 'A'.
    EXIT.
  ENDIF.
ENDLOOP.
```
