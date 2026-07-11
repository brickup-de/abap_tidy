---
title: "Access table index"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#access-table-index"
---

Access a specific index of an internal table directly, use the bracket notation `table_name[ ]`.

```ABAP
DATA(id_of_account_5) = accounts[ 5 ]-id.
```

Old style:

```ABAP
READ TABLE accounts INDEX 5 INTO DATA(account_5).
IF sy-subrc = 0.
  DATA(id_of_account_5) = account_5-id.
ENDIF.
```
