---
title: "CHECK vs. RETURN"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#check-vs-return"
---

There is no consensus on whether you should use `CHECK` or `RETURN` to exit a method
if the input doesn't meet expectations.

While `CHECK` definitely provides the shorter syntax

```ABAP
METHOD read_customizing.
  CHECK keys IS NOT INITIAL.
  " do whatever needs doing
ENDMETHOD.
```

the statement's name doesn't reveal what happens if the condition fails,
such that people will probably understand the long form better:

```ABAP
METHOD read_customizing.
  IF keys IS INITIAL.
    RETURN.
  ENDIF.
  " do whatever needs doing
ENDMETHOD.
```

You could avoid the question completely by reversing the validation and adopting a single-return control flow.
This is considered to be an anti-pattern because it introduces unnecessary nesting depth.

```ABAP
METHOD read_customizing.
  " anti-pattern
  IF keys IS NOT INITIAL.
    " do whatever needs doing
  ENDIF.
ENDMETHOD.
```

In any case, consider whether returning nothing is really the appropriate behavior.
Methods should provide a meaningful result, meaning either a filled return parameter, or an exception.
Returning nothing is in many cases similar to returning `null`, which should be avoided.

> The [section _Exiting Procedures_ in the ABAP Programming Guidelines](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/index.htm?file=abenexit_procedure_guidl.htm)
> recommends using `CHECK` in this instance.
> Community discussion suggests that the statement is so unclear
> that many people will not understand the program's behavior.
