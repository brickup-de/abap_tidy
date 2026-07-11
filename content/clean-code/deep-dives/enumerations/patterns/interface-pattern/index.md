---
title: "Interface Pattern"
linkTitle: "Interface"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#interface-pattern"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [Patterns](/clean-code/deep-dives/enumerations/patterns/) > [This section](/clean-code/deep-dives/enumerations/patterns/interface-pattern/)

```ABAP
" inferior pattern
INTERFACE /dirty/message_severity.
  CONSTANTS:
    warning TYPE symsgty VALUE 'W',
    error   TYPE symsgty VALUE 'E'.
ENDINTERFACE.
```

used as

```ABAP
IF log_contains( /dirty/message_severity=>warning ).
```
