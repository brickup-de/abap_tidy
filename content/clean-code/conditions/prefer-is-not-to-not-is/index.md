---
title: "Prefer IS NOT to NOT IS"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-is-not-to-not-is"
---

```ABAP
IF variable IS NOT INITIAL.
IF variable NP 'TODO*'.
IF variable <> 42.
```

Negation is logically equivalent
but requires a "mental turnaround"
that makes it harder to understand.

```ABAP
" anti-pattern
IF NOT variable IS INITIAL.
IF NOT variable CP 'TODO*'.
IF NOT variable = 42.
```

> A more specific variant of
[Try to make conditions positive](/clean-code/conditions/try-to-make-conditions-positive/).
Also as described in the section
[Alternative Language Constructs](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/index.htm?file=abenalternative_langu_guidl.htm)
in the ABAP programming guidelines.
