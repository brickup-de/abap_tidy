---
title: "Mind the legacy"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#mind-the-legacy"
---

If you code for older ABAP releases, take the advice in this guide with care:
Many recommendations on this site make use of relatively new syntax and constructs
that may not be supported in older ABAP releases.
Validate the guidelines you want to follow on the oldest release you must support.
Do not simply discard Clean Code as a whole -
the vast majority of rules (e.g. naming, commenting) will work in _any_ ABAP version.
