---
title: "Name the code under test meaningfully, or default to CUT"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#name-the-code-under-test-meaningfully-or-default-to-cut"
---

Give the variable that represents the code under test a meaningful name:

```ABAP
DATA blog_post TYPE REF TO ...
```

Don't just repeat the class name with all its non-valuable namespaces and prefixes:

```ABAP
" anti-pattern
DATA clean_fra_blog_post TYPE REF TO ...
```

If you have different test setups, it can be helpful to describe the object's varying state:

```ABAP
DATA empty_blog_post TYPE REF TO ...
DATA simple_blog_post TYPE REF TO ...
DATA very_long_blog_post TYPE REF TO ...
```

If you have problems finding a meaningful name, resort to `cut` as a default.
The abbreviation stands for "code under test".

```ABAP
DATA cut TYPE REF TO ...
```

Especially in unclean and confusing tests, calling the variable `cut`
can temporarily help the reader see what's actually tested.
However, tidying up the tests is the actual way to go for the long run.
