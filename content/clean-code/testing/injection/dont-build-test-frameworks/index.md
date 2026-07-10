---
title: "Don't build test frameworks"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-build-test-frameworks"
---

Unit tests - in contrast to integration tests - should be data-in-data-out, with all test data being defined on the fly as needed.

```ABAP
cl_abap_testdouble=>configure_call( test_double )->returning( data ).
```

Don't start building frameworks that distinguish "*test case IDs*" to decide what data to provide.
The resulting code will be so long and tangled that you won't be able to keep these tests alive in the long term.

```ABAP
" anti-pattern

test_double->set_test_case( 1 ).

CASE test_case.
  WHEN 1.
  WHEN 2.
ENDCASE.
```
