---
title: "Use FAIL to check for expected exceptions"
weight: 50
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-fail-to-check-for-expected-exceptions"
---

```ABAP
METHOD throws_on_empty_input.
  TRY.
      " when
      cut->do_something( '' ).
      cl_abap_unit_assert=>fail( ).
    CATCH /clean/some_exception.
      " then
  ENDTRY.
ENDMETHOD.
```
