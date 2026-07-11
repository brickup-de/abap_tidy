---
title: "Non-Initial Conditions"
weight: 40
params:
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
