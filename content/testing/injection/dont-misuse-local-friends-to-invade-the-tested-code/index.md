---
title: "Don't misuse LOCAL FRIENDS to invade the tested code"
linkTitle: "Don't misuse LOCAL FRIENDS"
weight: 60
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-misuse-local-friends-to-invade-the-tested-code"
---

Unit tests that access private and protected members to insert mock data are fragile:
they break when the internal structure of the tested code changes.

```ABAP
" anti-pattern
CLASS /dirty/class_under_test DEFINITION LOCAL FRIENDS unit_tests.
CLASS unit_tests IMPLEMENTATION.
  METHOD returns_right_result.
    cut->some_private_member = 'AUNIT_DUMMY'.
  ENDMETHOD.
ENDCLASS.
```
