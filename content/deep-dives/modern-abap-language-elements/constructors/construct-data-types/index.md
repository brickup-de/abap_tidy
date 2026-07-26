---
title: "Construct data types"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#construct-data-types"
---

Construct structures and tables using the `VALUE #( )` operator.
It also constructs initial values for most data types.

> This statement is a life saver when writing ABAP unit tests.

Structure:

```ABAP
DATA(account) = VALUE account_structure( id = 5
                                         name = 'SAP' ).
```

Old style:

```ABAP
DATA account TYPE account_structure.
account-id = 5.
account-name = 'SAP'.
```

Table:

```ABAP
DATA(accounts) = VALUE accounts_table( ( id = 5  name = 'SAP' )
                                       ( id = 6  name = 'ABCDE' ) ).
```

Old style:

```ABAP
DATA accounts TYPE accounts_table.
DATA account TYPE account_structure.
account-id = 5.
account-name = 'SAP'.
INSERT account INTO TABLE accounts.
account-id = 6.
account-name = 'ABCDE'.
INSERT ACCOUNT INTO TABLE accounts.
```

Construct tables based on other tables:

```ABAP
result = VALUE #( FOR row IN input ( row-text ) ).
```

Old style:

```ABAP
LOOP AT input INTO DATA(row).
  INSERT row-text INTO TABLE result.
ENDLOOP.
```
