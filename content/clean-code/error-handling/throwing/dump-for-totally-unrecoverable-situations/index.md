---
title: "Dump for totally unrecoverable situations"
weight: 70
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dump-for-totally-unrecoverable-situations"
---

If a situation is so severe that you are totally sure the receiver is unlikely to recover from it,
or that clearly indicates a programming error, dump instead of throwing an exception:
failure to acquire memory, failed index reads on a table that must be filled, etc.

```ABAP
RAISE SHORTDUMP TYPE cx_sy_create_object_error.  " >= NW 7.53
MESSAGE x666(general).                           " < NW 7.53
```

This behavior will prevent any kind of consumer from doing anything useful afterwards.
Use this only if you are sure about that.
