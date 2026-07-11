---
title: "Conditional distinction"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
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
