---
title: "Prefer LOOP AT WHERE to nested IF"
linkTitle: "Prefer LOOP WHERE to nested IF"
weight: 60
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-loop-at-where-to-nested-if"
---

```ABAP
LOOP AT my_table REFERENCE INTO DATA(line) WHERE key = 'A'.
```

expresses the intent clearer and shorter than

```ABAP
LOOP AT my_table REFERENCE INTO DATA(line).
  IF line->key = 'A'.
    EXIT.
  ENDIF.
ENDLOOP.
```
