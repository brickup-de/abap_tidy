---
title: "Compound Assignment Operators"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#compound-assignment-operators"
---

SAP NetWeaver 7.54 introduces shorthand versions
for arithmetic assignments and string concatenation.
These assignments also allow expressions in the operand position.

Shorthand | Longhand  |
---|---|
x += 1.  | x = x + 1.  |
x -= 1.  | x = x - 1.  |
x *= 1.  | x = x * 1.  |
x /= 1.  | x = x / 1.  |
x &&= \`abc\`. | x = x && \`abc\`. |
