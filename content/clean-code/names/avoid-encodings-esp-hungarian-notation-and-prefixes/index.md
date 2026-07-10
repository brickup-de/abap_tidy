---
title: "Avoid encodings, esp. Hungarian notation and prefixes"
weight: 120
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#avoid-encodings-esp-hungarian-notation-and-prefixes"
---

We encourage you to get rid of _all_ encoding prefixes.

```ABAP
METHOD add_two_numbers.
  result = a + b.
ENDMETHOD.
```

instead of the needlessly longer

```ABAP
METHOD add_two_numbers.
  rv_result = iv_a + iv_b.
ENDMETHOD.
```

> [Avoid Encodings](/clean-code/sub-sections-avoid-encodings-md/)
> describes the reasoning in depth.
