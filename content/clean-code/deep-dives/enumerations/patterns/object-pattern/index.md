---
title: "Object Pattern"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#object-pattern"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [Patterns](/clean-code/deep-dives/enumerations/patterns/) > [This section](/clean-code/deep-dives/enumerations/patterns/object-pattern/)

```ABAP
CLASS /clean/message_severity DEFINITION PUBLIC CREATE PRIVATE FINAL.

  PUBLIC SECTION.

    CLASS-DATA warning TYPE REF TO /clean/message_severity READ-ONLY,
    CLASS-DATA error   TYPE REF TO /clean/message_severity READ-ONLY.

    DATA value TYPE symsgty READ-ONLY.

    CLASS-METHODS class_constructor.
    METHODS constructor IMPORTING value TYPE symsgty.

ENDCLASS.

CLASS /clean/message_severity IMPLEMENTATION.

  METHOD class_constructor.
    warning = NEW /clean/message_severity( 'W' ).
    error = NEW /clean/message_severity( 'E' ).
  ENDMETHOD.

  METHOD constructor.
    me->value = value.
  ENDMETHOD.

ENDCLASS.
```

used in a type-safe way as follows:

```ABAP
" modern signature: ... IMPORTING severity TYPE REF TO /clean/message_severity ...
IF log_contains( /clean/message_severity=>warning ).
```

In legacy code where existing signatures cannot be refactored the property `value` must be accessed and used to satisfy the legacy method parameter type:

```ABAP
" legacy signature: ... IMPORTING severity TYPE symsgty ...
IF log_contains( /clean/message_severity=>warning->value ).
```
