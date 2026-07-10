---
title: "Weak substitution"
weight: 40
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/FunctionGroupsVsClasses.md#weak-substitution"
---

You can store function names in variables and call them dynamically,
allowing you to redirect calls to other functions with identical signature.

```ABAP
DATA function_name TYPE char30.
CALL FUNCTION function_name [...]
```

This needs to be planned, though, and does not come as naturally
as in object-oriented designs, making it harder to implement design patterns
that overwrite methods, such as [Decorator](https://en.wikipedia.org/wiki/Decorator_pattern).
