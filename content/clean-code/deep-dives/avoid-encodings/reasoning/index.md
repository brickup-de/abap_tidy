---
title: "Reasoning"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/AvoidEncodings.md#reasoning"
---

With ABAP there is a legacy practice of adding prefixes to each and everything, to encode things like

- `cl_` for classes
- `if_` for interfaces
- `is_` for an importing parameter
- `mo_` for a class member attribute
- `lt_` for a table-like variable
- `sc_` for a constant
- ...

This kind of prefixing is a relic from the early days of programming, when code was printed out and read on paper,
and you didn't want to flip around just to find some variable's type.
Modern development environments give easy access to data types, signatures, and object navigation,
such that it is no longer needed to get readable code.
