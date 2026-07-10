---
title: "Access table key with uncertain result"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#access-table-key-with-uncertain-result"
---

```ABAP
DATA(account) = VALUE #( accounts[ id = '4711' ] OPTIONAL ).
```

By default, failing functional key accesses throw an exception.
The addition `VALUE ... OPTIONAL` suppresses this.

Old style:

```ABAP
TRY.
    account = accounts[ id = '4711' ]
  CATCH cx_sy_itab_line_not_found.
ENDTRY.
```
