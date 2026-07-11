---
title: "Prefer basis checks to regular expressions"
linkTitle: "Prefer basis checks"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-basis-checks-to-regular-expressions"
---

```ABAP
CALL FUNCTION 'SEO_CLIF_CHECK_NAME'
  EXPORTING
    cls_name = class_name
  EXCEPTIONS
    ...
```

instead of reinventing things

```ABAP
" anti-pattern
DATA(is_valid) = matches( val     = class_name
                          pattern = '[A-Z][A-Z0-9_]{0,29}' ).
```

> There seems to be a natural tendency to turn blind to the Don't-Repeat-Yourself (DRY) principle
> when there are regular expressions around,
> compare section _Chapter 17: Smells and Heuristics: General: G5: Duplication_ in [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
