---
title: "Don't obsess with separating blank lines"
linkTitle: "Don't obsess with blank lines"
weight: 90
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-obsess-with-separating-blank-lines"
---

```ABAP
METHOD do_something.
  do_this( ).
  then_that( ).
ENDMETHOD.
```

No reason for the bad habit to tear your code apart with blank lines

```ABAP
" anti-pattern
METHOD do_something.

  do_this( ).

  then_that( ).

ENDMETHOD.
```

This is also the case within a statement, as this can easily be misunderstood as a new statement when skimming through the code.
```abap
" anti-pattern
DATA(result) = merge_structures( a = VALUE #( field_1 = 'X'
                                              field_2 = 'A' )

                                 b = NEW /clean/structure_type( field_3 = 'C'
                                                                field_4 = 'D' ) ).
```

Blank lines actually only make sense if you have statements that span multiple lines

```ABAP
METHOD do_something.

  do_this( ).

  then_that(
    EXPORTING
      variable = 'A'
    IMPORTING
      result   = result ).

ENDMETHOD.
```
