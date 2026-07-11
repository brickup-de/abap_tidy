---
title: "Write comments to explain the why, not the what"
weight: 40
params:
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
