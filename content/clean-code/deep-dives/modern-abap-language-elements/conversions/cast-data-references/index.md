---
title: "Cast data references"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#cast-data-references"
---

Cast reference types to other reference types using the `CAST #( )` operator.

```ABAP
DATA(my_account) = CAST account( NEW bank_account( ) ).
```

Old style:

```ABAP
DATA my_account TYPE REF TO account.
CREATE OBJECT my_account TYPE bank_account.
```

or

```ABAP
DATA my_account TYPE REF TO account.
DATA my_bank_account TYPE REF TO bank_account.
CREATE OBJECT my_bank_account.
my_account ?= bank_account.
```
