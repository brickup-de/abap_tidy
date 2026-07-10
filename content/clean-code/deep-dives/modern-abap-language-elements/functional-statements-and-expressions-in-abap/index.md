---
title: "Functional statements and expressions in ABAP"
weight: 60
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#functional-statements-and-expressions-in-abap"
---

Functional statements and expressions
have the advantage that they follow the principle of an assignment,
meaning the result is returned as a returning parameter,
thus can be directly used in assignments and can be chained.

Data type information in functional statements
can be abbreviated by a `#`
if the compiler can determine the data type from the context.

> **Keep the clean code principles in mind**
> when using these statements.
> They are very compact and powerful and may tempt you to
> compress your code so much that it becomes unintelligible.
