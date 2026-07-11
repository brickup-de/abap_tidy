---
title: "Use one development object per enumeration"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#use-one-development-object-per-enumeration"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [Guidelines](/clean-code/deep-dives/enumerations/guidelines/) > [This section](/clean-code/deep-dives/enumerations/guidelines/use-one-development-object-per-enumeration/)

```ABAP
CLASS /clean/message_severity DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    CONSTANTS:
      warning TYPE symsgty VALUE 'W',
      error   TYPE symsgty VALUE 'E'.
ENDCLASS.

CLASS /clean/document_type DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    CONSTANTS:
      sales_order    TYPE char02 VALUE '01',
      purchase_order TYPE char02 VALUE '02'.
ENDCLASS.
```

This simplifies searching for enumerations
because you can search for the name of the development object
instead of hassling with where-used lists and fulltext code searches.

Effective search is important as observations suggest
that being unable to find the required enumeration
causes people to quickly create constants
a second and third time in different places,
violating the don't-repeat-yourself principle. 

Separate development objects also improve cohesion of your classes
because consumers depend only on exactly what they need,
not some other enumerations that only accidentally happen
to reside in the same development object.

```ABAP
" anti-pattern
CLASS /dirty/common_constants DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    CONSTANTS:
      BEGIN OF message_severity,
        warning TYPE symsgty VALUE 'W',
        error   TYPE symsgty VALUE 'E',
      END OF message_severity,
      BEGIN OF document_type,
        sales_order    TYPE char02 VALUE '01',
        purchase_order TYPE char02 VALUE '02',
      END OF document_type.
ENDCLASS.
```
