---
title: "Filter tables"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#filter-tables"
---

Construct a table as a subset of another table using `FILTER #( )`.

```ABAP
bank_accounts = FILTER #( accounts
                          WHERE account_type = 'B' ).
```

Old style:

```ABAP
DATA bank_account TYPE bank_account.
LOOP AT accounts INTO bank_account WHERE account_type = 'B'.
  INSERT bank_account INTO TABLE bank_accounts.
ENDLOOP.
```
