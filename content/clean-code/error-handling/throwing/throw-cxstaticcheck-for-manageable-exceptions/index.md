---
title: "Throw CX_STATIC_CHECK for manageable exceptions"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#throw-cxstaticcheck-for-manageable-exceptions"
---

If an exception can be expected to occur and be reasonably handled by the receiver,
throw a checked exception inheriting from `CX_STATIC_CHECK`: failing user input validation,
missing resource for which there are fallbacks, etc.

```ABAP
CLASS cx_file_not_found DEFINITION INHERITING FROM cx_static_check.

METHODS read_file
  IMPORTING
    file_name_enterd_by_user TYPE string
  RAISING
    cx_file_not_found.
```

This exception type _must_ be given in method signatures and _must_ be caught or forwarded to avoid syntax errors.
It is therefore plain to see for the consumer and ensures that (s)he won't be surprised by an unexpected exception
and will take care of reacting to the error situation.

> This is in sync with the [ABAP Programming Guidelines](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abenexception_category_guidl.htm)
> but contradicts [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/),
> which recommends to prefer unchecked exceptions;
> [Exceptions](/clean-code/deep-dives/exceptions/) explains why.
