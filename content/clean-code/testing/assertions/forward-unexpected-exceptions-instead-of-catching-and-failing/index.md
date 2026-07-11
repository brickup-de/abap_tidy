---
title: "Forward unexpected exceptions instead of catching and failing"
weight: 60
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#forward-unexpected-exceptions-instead-of-catching-and-failing"
---

```ABAP
METHODS reads_entry FOR TESTING RAISING /clean/some_exception.

METHOD reads_entry.
  "when
  DATA(entry) = cut->read_something( ).
  "then
  cl_abap_unit_assert=>assert_not_initial( entry ).
ENDMETHOD.
```

Your test code remains focused on the happy path and is therefore much easier to read and understand, as compared to:

```ABAP
" anti-pattern
METHOD reads_entry.
  TRY.
      DATA(entry) = cut->read_something( ).
    CATCH /clean/some_exception INTO DATA(unexpected_exception).
      cl_abap_unit_assert=>fail( unexpected_exception->get_text( ) ).
  ENDTRY.
  cl_abap_unit_assert=>assert_not_initial( entry ).
ENDMETHOD.
```
