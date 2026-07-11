---
title: "Members PRIVATE by default, PROTECTED only if needed"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#members-private-by-default-protected-only-if-needed"
---

Make attributes, methods, and other class members `PRIVATE` by default.

Make them only `PROTECTED` if you want to enable sub-classes that override them.

Internals of classes should be made available to others only on a need-to-know basis.
This includes not only outside callers but also sub-classes.
Making information over-available can cause subtle errors by unexpected redefinitions and hinder refactoring
because outsiders freeze members in place that should still be liquid.
