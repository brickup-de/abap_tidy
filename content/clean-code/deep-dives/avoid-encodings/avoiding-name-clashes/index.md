---
title: "Avoiding name clashes"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/AvoidEncodings.md#avoiding-name-clashes"
---

One consequence of removing the prefixes is a potential name clash of entities which are in the the same namespace. So far it was a common practice to have interfaces and classes named identical, only differentiated by the prefix.

While this practice was not correct in the first place, as an interface is something more generic than an implementing class, there is now the need to be more precise in the naming of entities.

Name the interface more generic and the implementing classes more specific:

```ABAP
INTERFACE game_board.
  ...
ENDINTERFACE.

CLASS game_board_as_list DEFINITION.
  PUBLIC SECTION.
    INTERFACES game_board.
  ...
ENDCLASS.

CLASS game_board_as_array DEFINITION.
  PUBLIC SECTION.
    INTERFACES game_board.
  ...
ENDCLASS.
```

To avoid name clashes with method e.g. importing parameters use the self reference `me->`:

```ABAP
CLASS game_board_as_list DEFINITION.
  PUBLIC SECTION.
    METHODS constructor
      IMPORTING x_dimension TYPE i
                y_dimension TYPE i.
  PRIVATE SECTION.
    DATA x_dimension TYPE i.
    DATA y_dimension TYPE i.
ENDCLASS.

CLASS game_board_as_list IMPLEMENTATION.
  METHOD constructor.
    me->x_dimension = x_dimension.
    me->y_dimension = y_dimension.
  ENDMETHOD.
ENDCLASS.
```

For tables and structures use singular and plural:

```ABAP
TYPES: BEGIN OF coordinate,
         x TYPE i,
         y TYPE i,
       END OF coordinate.
TYPE coordinates TYPE STANDARD TABLE OF coordinate WITH DEFAULT KEY.
```
