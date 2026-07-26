---
title: "Indent in-line declarations like method calls"
weight: 190
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#indent-in-line-declarations-like-method-calls"
---

Indent in-line declarations with VALUE or NEW as if they were method calls:

```ABAP
DATA(result) = merge_structures( a = VALUE #( field_1 = 'X'
                                              field_2 = 'A' )
                                 b = NEW /clean/structure_type( field_3 = 'C'
                                                                field_4 = 'D' ) ).
```
