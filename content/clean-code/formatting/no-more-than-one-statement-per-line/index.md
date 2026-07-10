---
title: "No more than one statement per line"
weight: 50
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#no-more-than-one-statement-per-line"
---

```ABAP
DATA do_this TYPE i.
do_this = input + 3.
```

Even if some occurrences may trick you into the misconception that this was readable:

```ABAP
" anti-pattern
DATA do_this TYPE i. do_this = input + 3.
```
