---
title: "No method encapsulation"
weight: 70
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/FunctionGroupsVsClasses.md#no-method-encapsulation"
---

While form routines allow you to organize your code,
you cannot hide them from the outside world.

They remain visible to regular statements like: 

```ABAP
PERFORM set_buffer_true
  IN PROGRAM <some_program>.
```

Classes allow you to make methods private,
preventing outside access.

> Originally [answered on StackOverflow](https://stackoverflow.com/questions/55243044/function-groups-vs-classes/55244019#55244019).
