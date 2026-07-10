---
title: "Add a single blank line to separate things, but not more"
weight: 80
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#add-a-single-blank-line-to-separate-things-but-not-more"
---

```ABAP
DATA(result) = do_something( ).

DATA(else) = calculate_this( result ).
```

to highlight that the two statements do different things. But there is no reason for

```ABAP
" anti-pattern
DATA(result) = do_something( ).



DATA(else) = calculate_this( result ).
```

The urge to add separating blank lines may be an indicator that your method doesn't [do one thing](/clean-code/methods/method-body/do-one-thing-do-it-well-do-it-only/).
