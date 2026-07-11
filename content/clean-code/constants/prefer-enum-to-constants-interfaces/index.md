---
title: "Prefer ENUM to constants interfaces"
linkTitle: "Prefer ENUM to constant interfaces"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-enum-to-constants-interfaces"
---

Use ABAP-native enumerations with `ENUM` (available in releases >= 7.51)

```ABAP
CLASS /clean/message_severity DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    TYPES: BEGIN OF ENUM type,
             warning,
             error,
           END OF ENUM type.
ENDCLASS.
```

instead of mixing unrelated things
or misleading people to the conclusion
that constants collections could be "implemented":

```ABAP
" anti-pattern
INTERFACE /dirty/common_constants.
  CONSTANTS:
    warning      TYPE symsgty VALUE 'W',
    transitional TYPE i       VALUE 1,
    error        TYPE symsgty VALUE 'E',
    persisted    TYPE i       VALUE 2.
ENDINTERFACE.
```

> [Enumerations](/clean-code/deep-dives/enumerations/)
> describes alternative enumeration patterns (also applicable to older releases that do not support `ENUM` yet)
> and discusses their advantages and disadvantages.
>
> Read more in _Chapter 17: Smells and Heuristics: J3: Constants versus Enums_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
