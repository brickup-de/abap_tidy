---
title: "Conditional distinction"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#conditional-distinction"
---

To evaluate conditions, use the `COND #( )` operator.

```ABAP
DATA(value) = COND #( WHEN status = open THEN 1
                      WHEN status = blocked THEN 3
                      ELSE 7 ).
```

Old style:

```ABAP
DATA value TYPE i.
IF status = open.
  value = 1.
ELSEIF status = blocked.
  value = 3.
ELSE.
  value = 7.
ENDIF.
```

> Alternatively you may use the [function `xsdbool( )`](/clean-code/booleans/use-xsdbool-to-set-boolean-variables/)
