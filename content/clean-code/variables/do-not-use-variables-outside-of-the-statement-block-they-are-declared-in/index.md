---
title: "Do not use variables outside of the statement block they are declared in"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#do-not-use-variables-outside-of-the-statement-block-they-are-declared-in"
---

```ABAP
" anti-pattern
IF has_entries = abap_true.
  DATA(value) = 1.
ELSE.
  value = 2.
ENDIF.
```

A variable declared in a statement block (like in an `IF` or `LOOP` block) is still available outside of this block in the code that follows it.
This is confusing for readers, especially if the method is longer and the declaration is not spotted immediately.

If the variable is required outside of the statement block it is declared in, declare it beforehand:

```ABAP
DATA value TYPE i.
IF has_entries = abap_true.
  value = 1.
ELSE.
  value = 2.
ENDIF.
```

> Read more in _Chapter 5: Formatting: Vertical Distance: Variable Declarations_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
