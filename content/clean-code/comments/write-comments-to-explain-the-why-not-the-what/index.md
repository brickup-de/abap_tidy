---
title: "Write comments to explain the why, not the what"
weight: 40
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#write-comments-to-explain-the-why-not-the-what"
---

```ABAP
" can't fail, existence of >= 1 row asserted above
DATA(first_line) = table[ 1 ].
```

Nobody needs repeating the code in natural language

```ABAP
" anti-pattern
" select alert root from database by key
SELECT * FROM d_alert_root WHERE key = key.
```
