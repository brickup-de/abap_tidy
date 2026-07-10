---
title: "Optimize for reading, not for writing"
weight: 20
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#optimize-for-reading-not-for-writing"
---

Developers spend most time _reading_ code.
Actually _writing_ code takes up a way smaller portion of the day.

As a consequence, you should optimize your code formatting for reading and debugging, not for writing.

For example, you should prefer

```ABAP
DATA:
  a TYPE b,
  c TYPE d,
  e TYPE f.
```

to hacks such as

```ABAP
" anti-pattern
DATA:
  a TYPE b
  ,c TYPE d
  ,e TYPE f.
```
