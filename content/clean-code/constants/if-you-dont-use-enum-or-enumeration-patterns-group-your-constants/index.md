---
title: "If you don't use ENUM or enumeration patterns, group your constants"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#if-you-dont-use-enum-or-enumeration-patterns-group-your-constants"
---

If you cannot use enumerations and have to collect constants in a loose way, for example in an interface, at least group them:

```ABAP
CONSTANTS:
  BEGIN OF message_severity,
    warning TYPE symsgty VALUE 'W',
    error   TYPE symsgty VALUE 'E',
  END OF message_severity,
  BEGIN OF message_lifespan,
    transitional TYPE i VALUE 1,
    persisted    TYPE i VALUE 2,
  END OF message_lifespan.
```

makes the relation clearer than

```ABAP
" Anti-pattern
CONSTANTS:
  warning      TYPE symsgty VALUE 'W',
  transitional TYPE i       VALUE 1,
  error        TYPE symsgty VALUE 'E',
  persisted    TYPE i       VALUE 2,
```

The group also allows you group-wise access, for example for input validation:

```ABAP
DO.
  ASSIGN message_severity-(sy-index) TO FIELD-SYMBOL(<constant>).
  IF sy-subrc IS INITIAL.
    IF input = <constant>.
      DATA(is_valid) = abap_true.
      RETURN.
    ENDIF.
  ELSE.
    RETURN.
  ENDIF.
ENDDO.
```

> Read more in _Chapter 17: Smells and Heuristics: G27: Structure over Convention_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
