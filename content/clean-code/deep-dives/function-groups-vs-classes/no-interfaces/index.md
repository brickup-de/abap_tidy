---
title: "No interfaces"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/FunctionGroupsVsClasses.md#no-interfaces"
---

You cannot provide two implementations for the same function group.
Prevents mocking function calls in unit tests without dedicated techniques such as test seams.

> You _can_ provide multiple functions with identical signatures
and exchange them at runtime with dynamic calls,
as described in [weak subsitution](/clean-code/deep-dives/function-groups-vs-classes/weak-substitution/).
However, there is no real language support for this
and incompatible changes become apparent only at run time.
Compare this to interfaces, where failure to comply
with the signature leads to a syntax error at design time.
