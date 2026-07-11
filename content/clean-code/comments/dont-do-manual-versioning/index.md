---
title: "Don't do manual versioning"
weight: 90
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-do-manual-versioning"
---

```ABAP
" anti-pattern
* ticket 800034775 ABC ++ Start
output = calculate_result( input ).
* ticket 800034775 ABC ++ End
```
Attribution comments tend to pollute the code and don't provide big benefits as versioning is already done by source code management. Transport order texts are much more suitable for describing why something was adapted.
