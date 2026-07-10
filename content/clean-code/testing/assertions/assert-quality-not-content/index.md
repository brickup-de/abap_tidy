---
title: "Assert quality, not content"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#assert-quality-not-content"
---

If you are interested in a meta quality of the result,
but not in the actual content itself, express that with a suitable assert:

```ABAP
assert_all_lines_shorter_than( actual_lines        = table
                               expected_max_length = 80 ).
```

Asserting the precise content obscures what you actually want to test.
It is also fragile because refactoring may produce a different
but perfectly acceptable result although it breaks all your too-precise unit tests.

```ABAP
" anti-pattern
assert_equals( act = table
               exp = VALUE string_table( ( `ABC` ) ( `DEF` ) ( `GHI` ) ) ).
```
