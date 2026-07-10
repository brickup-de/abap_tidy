---
title: "Non-Initial Conditions"
weight: 60
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#non-initial-conditions"
---

The comparison `IS INITIAL` can be omitted in certain places.
This can, for example, be used to shorten Boolean comparisons:

```ABAP
IF is_valid( ).
  " method returned abap_true
ELSE.
  " method returned abap_false
ENDIF.
```
