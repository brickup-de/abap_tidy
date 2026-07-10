---
title: "Case distinction"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#case-distinction"
---

Evaluate case distinction with the `SWITCH #( )` operator

```ABAP
DATA(status) = SWITCH #( scrum_status
    WHEN scrum_status_open THEN status_waiting
    WHEN scrum_status_in_process THEN status_busy
    WHEN scrum_status_blocked THEN status_alarm
    WHEN scrum_status_done THEN status_ok ).
```

Old style:

```ABAP
DATA status TYPE status_enum.
CASE scrum_status.
  WHEN scrum_status_open.
    status = status_waiting.
  WHEN scrum_status_in_process.
    status = status_busy.
  WHEN scrum_status_blocked.
    status = status_alarm.
  WHEN scrum_status_done.
    status = status_ok.
ENDCASE.
```
