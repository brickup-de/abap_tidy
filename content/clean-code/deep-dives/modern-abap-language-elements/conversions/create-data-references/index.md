---
title: "Create data references"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#create-data-references"
---

Create data references to structures and tables with the operator `REF #( )`.

```ABAP
DATA accounts TYPE accounts_table.
import_accounts_references( REF #( accounts ) ).
```

Old style:

```ABAP
DATA accounts TYPE accounts_table.
DATA accounts_reference TYPE REF TO accounts_type.
GET REFERENCE OF accounts INTO accounts_reference.
import_accounts_references( accounts_reference ).
```
