---
title: "Make messages easy to find"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#make-messages-easy-to-find"
---

To make messages easy to find through a where-used search from transaction SE91, use the following pattern:

```ABAP
MESSAGE e001(ad) INTO DATA(message).
```

In case variable `message` is not needed, add the pragma `##NEEDED`:

```ABAP
MESSAGE e001(ad) INTO DATA(message) ##NEEDED.
```

Avoid the following:

```ABAP
" anti-pattern
IF 1 = 2. MESSAGE e001(ad). ENDIF.
```

This is an anti-pattern since:
- It contains unreachable code.
- It tests a condition which can never be true for equality.
