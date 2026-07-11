---
title: "Partially implement interfaces in tests"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#partially-implement-interfaces-in-tests"
---

Implement in tests for e.g. test doubles only the interface methods which you need and skip the not needed with the `PARTIALLY IMPLEMENTED` extension of the `INTERFACES` statement.

```ABAP
INTERFACE account.
  METHODS add_account IMPORTING account TYPE account.
  METHODS delete_account IMPORTING account_id TYPE account_id.
  METHODS get_account IMPORTING account_id TYPE account_id
                      RETURNING VALUE(result) TYPE account.
ENDINTERFACE.

CLASS test_double DEFINITION FOR TESTING.
  PUBLIC SECTION.
  INTERFACES account PARTIALLY IMPLEMENTED.
  DATA account_stub TYPE account.
ENDCLASS.

CLASS test_double IMPLEMENTATION.
  METHOD productive~get.
    result = account_stub.
  ENDMETHOD.
ENDCLASS.
```
