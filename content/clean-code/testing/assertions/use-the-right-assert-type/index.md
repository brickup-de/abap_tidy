---
title: "Use the right assert type"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-the-right-assert-type"
---

```ABAP
cl_abap_unit_assert=>assert_equals( act = table
                                    exp = test_data ).
```

Asserts often do more than meets the eye, for example `assert_equals`
includes type matching and providing precise descriptions if values differ.
Using the wrong, too-common asserts will force you into the debugger immediately
instead of allowing you to see what is wrong right from the error message.

```ABAP
" anti-pattern
cl_abap_unit_assert=>assert_true( xsdbool( act = exp ) ).
```
