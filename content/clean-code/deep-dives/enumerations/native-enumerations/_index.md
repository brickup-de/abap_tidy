---
title: "Native enumerations"
linkTitle: "Native"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#native-enumerations"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [This section](/clean-code/deep-dives/enumerations/native-enumerations/)

Starting with release 7.51 ABAP offers a native definition of enumerated types with `TYPES BEGIN OF ENUM`.

```ABAP
CLASS /clean/message_severity DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    TYPES: BEGIN OF ENUM type,
             warning,
             error,
           END OF ENUM type.
ENDCLASS.

CLASS /clean/message_severity IMPLEMENTATION.
ENDCLASS.
```

used as

```ABAP
IF log_contains( /clean/message_severity=>warning ).
```

> Note that the [`STRUCTURE` addition](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/index.htm?file=abaptypes_enum.htm#!ABAP_ADDITION_1@1@) **is not used**.
>
> One reason is that this would widen the API surface without the requiremend to do so.
> If the definition was `BEGIN OF ENUM type STRUCTURE severity` then `/dirty/message_severity=>severity` could be copied and passed around which is undesirable.
>
> Another reason is the additional grouping level that `STRUCTURE` introduces:
> If an enumeration value is used there is duplication that does not bring any semantic benefit:
> `/dirty/message_severity=>severity-warning` for example repeats the word "_severity_".
> A rather short-sighted reaction could be cutting that word from the class name.
> The remaining `/dirty/message=>severity`, however, misleads as for the purpose of the class `/dirty/message` - after all it deals only with message severities and not with messages in general.
> If further enumerations were to be added to that class its purpose would become unclear thus violating the single-responsibility principle.
>
> Thus declaring exactly one enumeration **without** `STRUCTURE` in a dedicated class should be preferred.
> It yields nicely addressable top-level enumeration values (see example at the beginning of this section).
> Prefer treating enumerations as first-class citizens and do not introduce unnecessary depth with structures.
