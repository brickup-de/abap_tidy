---
title: "Try to enforce type safety"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#try-to-enforce-type-safety"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [Guidelines](/clean-code/deep-dives/enumerations/guidelines/) > [This section](/clean-code/deep-dives/enumerations/guidelines/try-to-enforce-type-safety/)

The real advantage of enumerations in programming languages
is not that they provide constants,
but that they provide _all_ constants,
meaning they enforce type safety
by making the compiler reject invalid values.

Native enumerated types fulfill this criterion as the following method definition
```ABAP
METHODS log_contains
  IMPORTING
    minimum_severity TYPE /clean/message_severity=>type.
```
will allow correct usage like this
```ABAP
IF log_contains( /clean/message_severity=>warning ).
```
yet reject invalid calls such as
```ABAP
" syntax error
IF log_contains( 'W' ).
```
```ABAP
" runtime error
IF log_contains( CONV /clean/message_severity=>type( 'B' ) ).
```

If native enumeration cannot be used this is only achievable by the **[object pattern](/clean-code/deep-dives/enumerations/patterns/object-pattern/)**:
```ABAP
METHODS log_contains
  IMPORTING
    minimum_severity TYPE REF TO /clean/message_severity.
```

Without type safety, you still get helpful constants
but will find yourself repeating `is_valid( )` validations
all over the place.

```ABAP
" inferior pattern...
METHODS log_contains
  IMPORTING
    minimum_severity TYPE symsgty.

" ...is not preventing illegal values:
IF log_contains( '?' ).
```
