---
title: "Weak variable encapsulation"
weight: 60
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/FunctionGroupsVsClasses.md#weak-variable-encapsulation"
---

Function groups seem to hide internal state in "private" variables.
This is usually good enough for everyday programming.

Looking closely however reveals that there is no real memory protection,
and the variables are open to intrusive statements.

```ABAP
ASSIGN ('(<report_name>)gv_global_variable')
  TO <field_symbol>`.
```

Classes do this better by preventing access to private object members. 
because they hide value on instance level with objects.
