---
title: "Use ABAP_TRUE and ABAP_FALSE for comparisons"
weight: 30
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-abaptrue-and-abapfalse-for-comparisons"
---

```ABAP
has_entries = abap_true.
IF has_entries = abap_false.
```

Don't use the character equivalents `'X'` and `' '` or `space`;
they make it hard to see that this is a Boolean expression:

```ABAP
" anti-pattern
has_entries = 'X'.
IF has_entries = space.
```

Avoid comparisons with `INITIAL` - it forces readers to recollect that `abap_bool`'s default is `abap_false`:

```ABAP
" anti-pattern
IF has_entries IS NOT INITIAL.
```

> ABAP may be the one single programming language that does not come with built-in "constants" for true and false.
> However, having them is imperative.
> This recommendation is based on the ABAP Programming Guidelines.
