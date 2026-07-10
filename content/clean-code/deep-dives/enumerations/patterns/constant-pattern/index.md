---
title: "Constant Pattern"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#constant-pattern"
---

> [Enumerations](/clean-code/deep-dives/enumerations/enumerations/) > [Patterns](/clean-code/deep-dives/enumerations/patterns/) > [This section](/clean-code/deep-dives/enumerations/patterns/constant-pattern/)

```ABAP
CLASS /clean/message_severity DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    CONSTANTS:
      warning TYPE symsgty VALUE 'W',
      error   TYPE symsgty VALUE 'E'.
ENDCLASS.

CLASS /clean/message_severity IMPLEMENTATION.
ENDCLASS.
```

used as

```ABAP
IF log_contains( /clean/message_severity=>warning ).
```
