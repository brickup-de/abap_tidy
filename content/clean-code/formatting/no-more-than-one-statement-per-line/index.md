---
title: "No more than one statement per line"
weight: 50
params:
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
