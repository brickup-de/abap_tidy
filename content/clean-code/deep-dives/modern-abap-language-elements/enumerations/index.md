---
title: "Enumerations"
weight: 60
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#enumerations"
---

Define [enumerations](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/abaptypes_enum.htm#!ABAP_ADDITION_1@1@) instead of using constants.

```ABAP
TYPES:
  BEGIN OF ENUM scrum_status_type,
    open,
    in_progress,
    blocked,
    done,
  END OF ENUM scrum_status_type.

DATA(scrum_status) = open.
```

Old style:

```ABAP
CONSTANTS scrum_status_open       TYPE i VALUE 1.
CONSTANTS scrum_status_in_process TYPE i VALUE 2.
CONSTANTS scrum_status_blocked    TYPE i VALUE 3.
CONSTANTS scrum_status_done       TYPE i VALUE 4.

DATA scrum status TYPE i.
scrum_status = scrum_status_open.
```
