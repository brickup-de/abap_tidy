---
title: "Construct objects and data"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#construct-objects-and-data"
---

Construct objects and data with the `NEW #( )` operator.

```ABAP
DATA(account) = NEW cl_account( ).

DATA(dref) = NEW struct_type( component_1 = 10
                              component_2 = 'a' ).
```

```ABAP
DATA(account) = CAST if_account( NEW cl_account( ) ).

DATA data_structure TYPE REF TO struct_type.
CREATE DATA data_structure.
data_reference->component_1 = 10.
data_reference->component_2 = 'a'.
```

Old style:

```ABAP
DATA account TYPE REF TO cl_account.
CREATE OBJECT account.
```

```ABAP
DATA account TYPE REF TO if_account.
CREATE OBJECT account TYPE cl_account.
```
