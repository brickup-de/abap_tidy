---
title: "Compromises"
weight: 30
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#compromises"
---

Community discussions suggest that
people rather accept refactoring cascades
than being surprised by undeclared exceptions.
As a consequence, we suggest to prefer checked exceptions
to unchecked ones in the way described in the guide.

A different sort of compromise is the mixed-case scenario:
use unchecked exceptions for _internal_ methods
that are fully under your team's control
and where people anticipate them,
and resort to checked exceptions for _borderline_ methods
that may be called from other stakeholders,
to clearly communicate where something can go wrong.
