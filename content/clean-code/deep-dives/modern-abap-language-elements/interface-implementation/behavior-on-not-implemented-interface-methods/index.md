---
title: "Behavior on not implemented interface methods"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#behavior-on-not-implemented-interface-methods"
---

Define the effect on not implemented interface methods.

Add `DEFAULT IGNORE` to advise ABAP to handle the call to this method if not implemented as a call to an empty implementation.

```ABAP
INTERFACE account.
  METHODS new_method DEFAULT IGNORE.
ENDINTERFACE.
```

Add `DEFAULT FAIL` to advise ABAP to raise an exception `CX_SY_DYN_CALL_ILLEGAL_METHOD` if the not implemented method is called. This is the default behavior.

```ABAP
INTERFACE account.
  METHODS new_method DEFAULT FAIL.
ENDINTERFACE.
```
