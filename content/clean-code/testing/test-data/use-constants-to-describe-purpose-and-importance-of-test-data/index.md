---
title: "Use constants to describe purpose and importance of test data"
linkTitle: "Use constants to describe purpose/importance"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-constants-to-describe-purpose-and-importance-of-test-data"
---

```ABAP
CONSTANTS some_nonsense_key TYPE char8 VALUE 'ABCDEFGH'.

METHOD throws_on_invalid_entry.
  TRY.
      " when
      cut->read_entry( some_nonsense_key ).
      cl_abap_unit_assert=>fail( ).
    CATCH /clean/customizing_reader_error.
      " then
  ENDTRY.
ENDMETHOD.
```
