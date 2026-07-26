---
title: "Delete code instead of commenting it"
weight: 80
params:
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
