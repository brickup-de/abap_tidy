---
title: "Compound Assignment Operators"
weight: 60
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
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
