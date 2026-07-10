---
title: "Case distinctions of reference types class and interface"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#case-distinctions-of-reference-types-class-and-interface"
---

Switch on a reference types class and interface using the `CASE` extension `TYPE OF`.

```ABAP
CASE TYPE OF account.
  WHEN TYPE bank_account INTO DATA(bank_account).
    " some processing ...
  WHEN OTHERS.
    " some processing ...
ENDCASE.
```

In a condition e.g. in an `IF` statement the `IS INSTANCE OF` operator can be used.

```ABAP
IF account IS INSTANCE OF bank_account.
  " some processing ...
ENDIF.
```
