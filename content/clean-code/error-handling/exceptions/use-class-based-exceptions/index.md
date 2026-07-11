---
title: "Use class-based exceptions"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-class-based-exceptions"
---

```ABAP
TRY.
    get_component_types( ).
  CATCH cx_has_deep_components_error.
ENDTRY.
```

The outdated non-class-based exceptions have the same features as return codes and shouldn't be used anymore.

```ABAP
" anti-pattern
get_component_types(
  EXCEPTIONS
    has_deep_components = 1
    OTHERS              = 2 ).
```
