---
title: "Call local test classes by their purpose"
linkTitle: "Naming by purpose"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#call-local-test-classes-by-their-purpose"
---

Name local test classes either by the "when" part of the story

```ABAP
CLASS ltc_<public method name> DEFINITION FOR TESTING ... ."
```

or the "given" part of the story

```ABAP
CLASS ltc_<common setup semantics> DEFINITION FOR TESTING ... .
```

```ABAP
" anti-patterns
CLASS ltc_fra_online_detection_api DEFINITION FOR TESTING ... . " We know that's the class under test - why repeat it?
CLASS ltc_test DEFINITION FOR TESTING ....                      " Of course it's a test, what else should it be?
```
