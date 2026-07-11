---
title: "Why CX_SY_NO_HANDLER Doesn't Help"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#why-cx_sy_no_handler-doesnt-help"
---

Catching the special exception `cx_sy_no_handler`
is a workaround that appears to get pretty near to the ideal way,
but also adds some imperfections that make it hard to recommend it:

```ABAP
METHOD upper_method.
  TRY.
      middle_method( ).
    CATCH cx_sy_no_handler INTO DATA(outer).
      DATA(inner) = outer->previous.
      " identify and branch on inner's type
  ENDTRY.
ENDMETHOD.
```

`cx_sy_no_handler` prevents using multiple `catch` branches
to handle different exceptions in different ways.

The code required to identify the actual exception -
either a series of trial-and-error casts,
or an [RTTI](https://help.sap.com/doc/abapdocu_752_index_htm/7.52/en-US/abenrtti.htm) request for the class name, followed by case branches -
is rather bulky and repetitive.

Catching `cx_sy_no_handler` everywhere also dilutes its original purpose -
to allow frameworks to handle bad plug-in code -
a case that you then may have to handle differently.
