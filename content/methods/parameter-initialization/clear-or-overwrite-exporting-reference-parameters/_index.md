---
title: "Clear or overwrite EXPORTING reference parameters"
linkTitle: "Clear EXPORTING reference parameters"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#clear-or-overwrite-exporting-reference-parameters"
---

Reference parameters refer to existing memory areas that may be filled beforehand.
Clear or overwrite them to provide reliable data:

```ABAP
METHODS square
  EXPORTING
    result TYPE i.

" clear
METHOD square.
  CLEAR result.
  " ...
ENDMETHOD.

" overwrite
METHOD square.
  result = cl_abap_math=>square( 2 ).
ENDMETHOD.
```

> Code inspector and Checkman point out `EXPORTING` variables that are never written.
Use these static checks to avoid this otherwise rather obscure error source.
