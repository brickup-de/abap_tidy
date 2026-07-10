---
title: "Use test seams as temporary workaround"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-test-seams-as-temporary-workaround"
---

If all other techniques fail, or when in dangerous shallow waters of legacy code,
refrain to [test seams](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/index.htm?file=abaptest-seam.htm)
to make things testable.

Although they look comfortable at first sight, test seams are invasive and tend to get entangled
in private dependencies, such that they are hard to keep alive and stable in the long run.

We therefore recommend to refrain to test seams only as a temporary workaround
to allow you refactoring the code into a more testable form.
