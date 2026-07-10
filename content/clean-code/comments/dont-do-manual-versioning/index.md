---
title: "Don't do manual versioning"
weight: 90
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-do-manual-versioning"
---

```ABAP
" anti-pattern
* ticket 800034775 ABC ++ Start
output = calculate_result( input ).
* ticket 800034775 ABC ++ End
```
Attribution comments tend to pollute the code and don't provide big benefits as versioning is already done by source code management. Transport order texts are much more suitable for describing why something was adapted.
