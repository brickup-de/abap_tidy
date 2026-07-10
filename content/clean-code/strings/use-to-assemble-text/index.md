---
title: "Use | to assemble text"
weight: 20
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-to-assemble-text"
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
