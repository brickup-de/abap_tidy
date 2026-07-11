---
title: "Why CX_STATIC_CHECK Doesn't Help"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Exceptions.md#why-cxstaticcheck-doesnt-help"
---

`cx_static_check` would force `middle_method`
to redeclare the `/clean/flexible_exception`.
Although the syntax check throws "only" a warning,
the ABAP Test Cockpit responds with an issue with Very High priority
that will prevent transport release in standard system setups.

Even if we were willing to accept these warnings,
without redeclaring `/clean/flexible_exception`,
`middle_method` would not forward it 
but trigger a `cx_sy_no_handler` exception
which ultimately leads to a dump.
