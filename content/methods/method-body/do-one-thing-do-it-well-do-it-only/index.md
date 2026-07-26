---
title: "Do one thing, do it well, do it only"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#do-one-thing-do-it-well-do-it-only"
---

A method should do one thing, and only one thing.
It should do it in the best way possible.

A method likely does one thing if

- it has [few input parameters](/methods/parameter-number/aim-for-few-importing-parameters-at-best-less-than-three/)
- it [doesn't include Boolean parameters](/methods/parameter-types/split-method-instead-of-boolean-input-parameter/)
- it has [exactly one output parameter](/methods/parameter-number/return-export-or-change-exactly-one-parameter/)
- it is [small](/methods/method-body/keep-methods-small/)
- it [descends one level of abstraction](/methods/method-body/descend-one-level-of-abstraction/)
- it only [throws one type of exception](/error-handling/throwing/throw-one-type-of-exception/)
- you cannot extract meaningful other methods
- you cannot meaningfully group its statements into sections
