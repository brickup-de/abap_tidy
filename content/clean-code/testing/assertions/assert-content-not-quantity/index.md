---
title: "Assert content, not quantity"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#assert-content-not-quantity"
---

```ABAP
assert_contains_exactly( actual   = table
                         expected = VALUE string_table( ( `ABC` ) ( `DEF` ) ( `GHI` ) ) ).
```

Don't write magic-number-quantity assertions if you can express the actual content you expect.
Numbers may vary although the expectations are still met.
In reverse, the numbers may match although the content is something completely unexpected.

```ABAP
" anti-pattern
assert_equals( act = lines( log_messages )
               exp = 3 ).
```
