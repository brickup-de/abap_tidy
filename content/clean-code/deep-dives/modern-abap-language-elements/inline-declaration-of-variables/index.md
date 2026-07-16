---
title: "Inline declaration of variables"
linkTitle: "Inline declaration"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#inline-declaration-of-variables"
---

Use the operators
[`DATA`](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/abendata_inline.htm)
and
[`FIELD-SYMBOL`](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-us/abenfield-symbol_inline.htm)
to combine the declaration and initial value assignment
of a variable or field symbol.

Allowed at write positions
for which a type can be determined
statically from the context.
This _inferred_ type is given to the declared symbol.

```ABAP
DATA(text) = `This is a string`.

" old style
DATA text TYPE string.
text = `This is a string`.
```

```ABAP
DATA(result) = method_with_returning( ).

" old style
DATA result TYPE accounts_table.
result = method_with_returning( ).
```

```ABAP
method_with_exporting( IMPORTING parameter = DATA(accounts) ).

" old style
DATA accounts TYPE accounts_table.
method_with_exporting( IMPORTING parameter = accounts ).
```

```ABAP
LOOP AT accounts INTO DATA(account).
ENDLOOP.

" old style
DATA account TYPE account_structure.
LOOP AT accounts INTO account.
ENDLOOP.
```

```ABAP
READ TABLE accounts INTO DATA(account_sap) WITH KEY id = 5.

" old style
DATA account_sap TYPE account_structure.
READ TABLE account INTO account_sap WITH u id = 5.
```

```ABAP
LOOP AT accounts ASSIGNING FIELD-SYMBOL(<account>).
ENDLOOP.

" old style
FIELD-SYMBOLS <account> TYPE account_structure.
LOOP AT accounts ASSIGNING (<account>).
ENDLOOP.
```

```ABAP
ASSIGN COMPONENT id OF account_sap TO FIELD-SYMBOL(<account_id>).

" old style
FIELD-SYMBOLS <account_id> TYPE account_id_type.
ASSIGN COMPONENT id OF account_sap TO <account_id>.
```

```ABAP
SELECT * FROM t000 INTO TABLE @DATA(clients).

" old style
DATA clients TYPE STANDARD TABLE OF t000.
SELECT * FROM t000 INTO TABLE clients.
```
