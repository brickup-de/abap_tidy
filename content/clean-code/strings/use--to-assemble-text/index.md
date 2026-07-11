---
title: "Use | to assemble text"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use--to-assemble-text"
---

```ABAP
DATA(message) = |Received HTTP code { status_code } with message { text }|.
```

String templates highlight better what's literal and what's variable,
especially if you embed multiple variables in a text.

```ABAP
" anti-pattern
DATA(message) = `Received an unexpected HTTP ` && status_code && ` with message ` && text.
```
