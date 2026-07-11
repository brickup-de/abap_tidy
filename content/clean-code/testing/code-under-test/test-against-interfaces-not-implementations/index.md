---
title: "Test against interfaces, not implementations"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#test-against-interfaces-not-implementations"
---

A practical consequence of the [_Test publics, not private internals_](/clean-code/testing/principles/test-publics-not-private-internals/),
type your code under test with an _interface_

```ABAP
DATA code_under_test TYPE REF TO some_interface.
```

rather than a _class_

```ABAP
" anti-pattern
DATA code_under_test TYPE REF TO some_class.
```
