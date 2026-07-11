---
title: "Do not chain up-front declarations"
linkTitle: "Don't chain up-front declarations"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#do-not-chain-up-front-declarations"
---

```ABAP
DATA name TYPE seoclsname.
DATA reader TYPE REF TO reader.
```

Chaining suggests the defined variables are related on a logical level.
To consistently use it, you would have to ensure that all chained variables belong together,
and introduce additional chain groups to add variables.
While this is possible, it is usually not worth the effort.

Chaining also needlessly complicates reformatting and refactoring
because each line looks different and changing them requires meddling with
colons, dots, and commas, that are not worth the effort.

```ABAP
" anti-pattern
DATA:
  name   TYPE seoclsname,
  reader TYPE REF TO reader.
```

> Also refer to [Don't align type clauses](/clean-code/formatting/dont-align-type-clauses/)  
> If chaining of data declaration is used, then use one chain for each group of variables belonging together.
