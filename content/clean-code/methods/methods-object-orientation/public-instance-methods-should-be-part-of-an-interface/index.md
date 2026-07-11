---
title: "Public instance methods should be part of an interface"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#public-instance-methods-should-be-part-of-an-interface"
---

Public instance methods should always be part of an interface.
This decouples dependencies and simplifies mocking them in unit tests.

```ABAP
METHOD /clean/blog_post~publish.
```

In clean object orientation, having a method public without an interface does not make much sense -
with few exceptions such as enumeration classes
which will never have an alternative implementation and will never be mocked in test cases.

> [Interfaces vs. abstract classes](/clean-code/deep-dives/interfaces-vs-abstract-classes/)
describes why this also applies to classes that overwrite inherited methods.
