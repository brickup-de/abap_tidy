---
title: "\"When\" is exactly one call"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#when-is-exactly-one-call"
---

Make sure that the "when" section of your test method contains exactly one call to the class under test:

```ABAP
METHOD rejects_invalid_input.
  " when
  DATA(is_valid) = cut->is_valid_input( 'SOME_RANDOM_ENTRY' ).
  " then
  cl_abap_unit_assert=>assert_false( is_valid ).
ENDMETHOD.
```

Calling multiple things indicates that the method has no clear focus and tests too much.
This makes it harder to find the cause when the test fails:
was it the first, second, or third call that caused the failure?
It also confuses the reader because he is not sure what the exact feature under test is.
