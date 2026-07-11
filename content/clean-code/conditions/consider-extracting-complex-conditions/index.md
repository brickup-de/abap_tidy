---
title: "Consider extracting complex conditions"
weight: 50
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#consider-extracting-complex-conditions"
---

It's nearly always a good idea to extract complex conditions to methods of their own:

```ABAP
IF is_provided( example ).

METHOD is_provided.
  DATA(is_filled) = xsdbool( example IS NOT INITIAL ).
  DATA(is_working) = xsdbool( applies( example ) = abap_true OR
                              fits( example ) = abap_true ).
  result = xsdbool( is_filled = abap_true AND
                    is_working = abap_true ).
ENDMETHOD.
```
