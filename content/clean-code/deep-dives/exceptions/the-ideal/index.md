---
title: "The Ideal"
weight: 30
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#the-ideal"
---

According to discussions in the community,
the optimal way to deal with exceptions would be as follows.

First, we want to declare the exception in
the `lower_method` that actually throws it,
to not surprise callers:


```ABAP
METHODS lower_method
  RAISING
    /clean/flexible_exception.

METHOD lower_method.
  RAISE EXCEPTION NEW /clean/flexible_exception( ).
ENDMETHOD:
```

Then we want to let the exception bubble upwards through `middle_method`s
without forcing them to redeclare or catch the exception,
to avoid refactoring cascades if exceptions change:

```ABAP
METHODS middle_method.

METHOD middle_method.
  lower_method( ).
ENDMETHOD.
```

Finally, we want to catch the exception in some `upper_method` and handle it.

```ABAP
METHODS upper_method.

METHOD upper_method.
  TRY.
      middle_method( ).
    CATCH /clean/flexible_exception.
      " ...
  ENDTRY.
ENDMETHOD.
```

This is also exactly what Robert C. Martin advertises for Java,
where this pattern can be implemented with [unchecked exceptions](https://docs.oracle.com/javase/7/docs/api/java/lang/RuntimeException.html).
