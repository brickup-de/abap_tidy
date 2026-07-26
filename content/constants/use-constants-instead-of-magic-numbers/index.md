---
title: "Use constants instead of magic numbers"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-constants-instead-of-magic-numbers"
---

```ABAP
IF abap_type = cl_abap_typedescr=>typekind_date.
```

is clearer than

```ABAP
" anti-pattern
IF abap_type = 'D'.
```

> Read more in _Chapter 17: Smells and Heuristics: G25:
> Replace Magic Numbers with Named Constants_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
