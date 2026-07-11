---
title: "Use PREFERRED PARAMETER sparingly"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-preferred-parameter-sparingly"
---

The addition `PREFERRED PARAMETER` makes it hard to see which parameter is actually supplied,
making it harder to understand the code.
Minimizing the number of parameters, especially optional ones,
automatically reduces the need for `PREFERRED PARAMETER`.
