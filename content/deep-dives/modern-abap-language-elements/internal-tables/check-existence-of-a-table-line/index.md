---
title: "Check existence of a table line"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#check-existence-of-a-table-line"
---

Check the existence of a line in an internal table,
use the function `line_exists( )` within an if-clause.

```ABAP
IF line_exists( accounts[ id = 4711 ] ).
  "line has been found
ENDIF.
```

Old style:

```ABAP
READ TABLE accounts WITH KEY id = 4711 TRANSPORTING NO FIELDS.
IF sy-subrc = 0.
  "line has been found
ENDIF.
```
