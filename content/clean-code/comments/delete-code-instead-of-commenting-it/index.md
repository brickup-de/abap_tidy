---
title: "Delete code instead of commenting it"
weight: 80
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#delete-code-instead-of-commenting-it"
---

```ABAP
" anti-pattern
* output = calculate_result( input ).
```

When you find something like this, delete it.
The code is obviously not needed because your application works and all tests are green.
Deleted code can be reproduced from the version history later on.
If you need to preserve a piece of code permanently, copy it to a file or a `$TMP` or `HOME` object.
