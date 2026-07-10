---
title: "Prefer exceptions to return codes"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-exceptions-to-return-codes"
---

```ABAP
METHOD try_this_and_that.
  RAISE EXCEPTION NEW cx_failed( ).
ENDMETHOD.
```

instead of

```ABAP
" anti-pattern
METHOD try_this_and_that.
  error_occurred = abap_true.
ENDMETHOD.
```

Exceptions have multiple advantages over return codes:

- Exceptions keep your method signatures clean:
you can return the result of the method as a `RETURNING` parameter and still throw exceptions alongside.
Return codes pollute your signatures with additional parameters for error handling.

- The caller doesn't have to react to them immediately.
He can simply write down the happy path of his code.
The exception-handling `CATCH` can be at the very end of his method, or completely outside.

- Exceptions can provide details on the error in their attributes and through methods.
Return codes require you to devise a different solution on your own, such as also returning a log.

- The environment reminds the caller with syntax errors to handle exceptions.
Return codes can be accidentally ignored without anybody noticing.
