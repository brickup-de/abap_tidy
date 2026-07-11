---
title: "Collection Pattern"
linkTitle: "Collection"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#collection-pattern"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [Patterns](/clean-code/deep-dives/enumerations/patterns/) > [This section](/clean-code/deep-dives/enumerations/patterns/collection-pattern/)

```ABAP
" inferior pattern
INTERFACE /dirty/message_constants.
  CONSTANTS:
    BEGIN OF message_severity,
      warning TYPE symsgty VALUE 'W',
      error   TYPE symsgty VALUE 'E',
    END OF message_severity,
    BEGIN OF message_lifecycle,
      transitional TYPE i VALUE 1,
      persisted    TYPE i VALUE 2,
    END OF message_lifecycle.
ENDINTERFACE.
```

used as

```ABAP
IF log_contains( /dirty/message_constants=>message_severity-warning ).
```
