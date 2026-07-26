---
title: "Loop with control break"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#loop-with-control-break"
---

Process data on defined groups using the new features with the `loop` statement extension `group by ...` and `loop at group`.

```ABAP
LOOP AT accounts INTO DATA(account) GROUP BY grouping_id.
  " once per group before group ...
  LOOP AT GROUP account INTO DATA(account_group).
    " for each group member ...
  ENDLOOP.
  " once per group after group ...
ENDLOOP.
```

Old style:

```ABAP
DATA previous_grouping_id TYPE i.
DATA last_account TYPE account.
LOOP AT accounts INTO data(account).
  IF account-grouping_id <> previous_grouping_id.
    previous_grouping_id = account-grouping_id
    " once per group before group ...
    IF last_account IS NOT INITIAL.
      " once per group after group ...
    ENDIF.
  ENDIF.
  " for each group member ...
  last_account = account.
ENDLOOP.
IF last_account IS NOT INITIAL.
  " once per group after group
ENDIF.
```
