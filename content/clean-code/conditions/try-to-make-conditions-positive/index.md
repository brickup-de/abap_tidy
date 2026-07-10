---
title: "Try to make conditions positive"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#try-to-make-conditions-positive"
---

```ABAP
IF has_entries = abap_true.
```

For comparison, see how hard to understand the same statement gets by reversing it:

```ABAP
" anti-pattern
IF has_no_entries = abap_false.
```

The "try" in the section title means you shouldn't force this
up to the point where you end up with something like [empty IF branches](/clean-code/ifs/no-empty-if-branches/):

```ABAP
" anti-pattern
IF has_entries = abap_true.
ELSE.
  " only do something in the ELSE block, IF remains empty
ENDIF.
```

> Read more in _Chapter 17: Smells and Heuristics: G29: Avoid Negative Conditionals_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
