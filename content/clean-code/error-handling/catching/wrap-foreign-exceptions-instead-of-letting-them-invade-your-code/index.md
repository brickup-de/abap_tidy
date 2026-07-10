---
title: "Wrap foreign exceptions instead of letting them invade your code"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#wrap-foreign-exceptions-instead-of-letting-them-invade-your-code"
---

```ABAP
METHODS generate RAISING cx_generation_failure.

METHOD generate.
  TRY.
      generator->generate( ).
    CATCH cx_amdp_generation_failure INTO DATA(exception).
      RAISE EXCEPTION NEW cx_generation_failure( previous = exception ).
  ENDTRY.
ENDMETHOD.
```

The [Law of Demeter](https://en.wikipedia.org/wiki/Law_of_Demeter) recommends de-coupling things.
Forwarding exceptions from other components violates this principle.
Make yourself independent from the foreign code by catching those exceptions
and wrapping them in an exception type of your own.

```ABAP
" anti-pattern
METHODS generate RAISING cx_sy_gateway_failure.

METHOD generate.
  generator->generate( ).
ENDMETHOD.
```
