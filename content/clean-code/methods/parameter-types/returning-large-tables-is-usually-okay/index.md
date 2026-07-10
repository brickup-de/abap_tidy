---
title: "RETURNING large tables is usually okay"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#returning-large-tables-is-usually-okay"
---

Although the ABAP language documentation and performance guides say otherwise,
we rarely encounter cases where handing over a large or deeply-nested table in a VALUE parameter
_really_ causes performance problems.
We therefore recommend to generally use

```ABAP
METHODS get_large_table
  RETURNING
    VALUE(result) TYPE /clean/some_table_type.

METHOD get_large_table.
  result = large_table.
ENDMETHOD.

DATA(my_table) = get_large_table( ).
```

Only if there is actual proof (= a bad performance measurement) for your individual case
should you resort to the more cumbersome procedural style

```ABAP
" anti-pattern
METHODS get_large_table
  EXPORTING
    result TYPE /dirty/some_table_type.

METHOD get_large_table.
  result = large_table.
ENDMETHOD.

get_large_table( IMPORTING result = DATA(my_table) ).
```

> This section contradicts the ABAP Programming Guidelines and Code Inspector checks,
> both of whom suggest that large tables should be EXPORTED by reference to avoid performance deficits.
> We consistently failed to reproduce any performance and memory deficits
> and received notice about kernel optimization that generally improves RETURNING performance,
> see [_Sharing Between Dynamic Data Objects_ in the ABAP Language Help](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abenmemory_consumption_3.htm).
