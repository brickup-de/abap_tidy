---
title: "Align assignments to the same object, but not to different ones"
weight: 100
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#align-assignments-to-the-same-object-but-not-to-different-ones"
---

To highlight that these things somehow belong together

```ABAP
structure-type = 'A'.
structure-id   = '4711'.
```

or even better

```ABAP
structure = VALUE #( type = 'A'
                     id   = '4711' ).
```

But leave things ragged that have nothing to do with each other:

```ABAP
customizing_reader = fra_cust_obj_model_reader=>s_get_instance( ).
hdb_access = fra_hdbr_access=>s_get_instance( ).
```

> Read more in _Chapter 5: Formatting: Horizontal Alignment_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
