---
title: "Prefer INSERT INTO TABLE to APPEND TO"
weight: 30
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-insert-into-table-to-append-to"
---

```ABAP
INSERT VALUE #( ... ) INTO TABLE itab.
```

`INSERT INTO TABLE` works with all table and key types,
thus making it easier for you to refactor the table's type and key definitions if your performance requirements change.

Use `APPEND TO` only if you use a `STANDARD` table in an array-like fashion,
if you want to stress that the added entry shall be the last row.
