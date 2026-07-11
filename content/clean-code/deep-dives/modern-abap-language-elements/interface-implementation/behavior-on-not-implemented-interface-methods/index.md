---
title: "Behavior on not implemented interface methods"
weight: 10
params:
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
