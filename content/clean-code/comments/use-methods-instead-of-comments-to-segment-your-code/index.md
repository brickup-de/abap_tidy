---
title: "Use methods instead of comments to segment your code"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-methods-instead-of-comments-to-segment-your-code"
---

```ABAP
DATA(statement) = build_statement( ).
DATA(data) = execute_statement( statement ).
```

This not only makes the intent, structure, and dependencies of the code much clearer,
it also avoids carry-over errors when temporary variables aren't properly cleared between the sections.

```ABAP
" anti-pattern
" -----------------
" Build statement
" -----------------
DATA statement TYPE string.
statement = |SELECT * FROM d_document_roots|.

" -----------------
" Execute statement
" -----------------
DATA(result_set) = adbc->execute_sql_query( statement ).
result_set->next_package( IMPORTING data = data ).
```
