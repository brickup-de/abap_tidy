---
title: "Constants also need descriptive names"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#constants-also-need-descriptive-names"
---

There is a historic tendency in ABAP to wrap every literal in constants, often with names 
that merely repeat their content or even just their type:
```ABAP
" anti-pattern 
CONSTANTS: 
  c_01 TYPE spart VALUE '01',
  c_mmsta TYPE mmsta VALUE '90'.
```
There is little benefit to either variant. It is not informative for the reader, and if 
the value ever needs to change then a constant named by its value must also be renamed. 

If a coded constant is declared in code then it should describe its meaning not its content.
```ABAP
CONSTANTS status_inactive TYPE mmsta VALUE '90'.
```
It is of course acceptable to repeat the constant's value if it is already descriptive enough: 
```ABAP
CONSTANTS status_cancelled TYPE sww_wistat value 'CANCELLED'.
```

> Note: This section is a specialization of [Use descriptive names](/clean-code/names/use-descriptive-names/), applied to constants.
