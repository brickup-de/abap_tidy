---
title: "Compound Assignment Operators"
linkTitle: "Compound Assignments"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#compound-assignment-operators"
---

SAP NetWeaver 7.54 introduces shorthand versions
for arithmetic assignments and string concatenation.
These assignments also allow expressions in the operand position.

```ABAP
x += 1. " short
x = x + 1. " long

x -= 1. " short
x = x - 1. " long

x *= 1. " short
x = x * 1. " long

x /= 1. " short
x = x / 1. " long

x &&= `abc`. " short
x = x && `abc`. " long
```
