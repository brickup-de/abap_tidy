---
title: "Consider assembling complex regular expressions"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#consider-assembling-complex-regular-expressions"
---

```ABAP
CONSTANTS class_name TYPE string VALUE `CL\_.*`.
CONSTANTS interface_name TYPE string VALUE `IF\_.*`.
DATA(object_name) = |{ class_name }\|{ interface_name }|.
```

Some complex regular expressions become easier
when you demonstrate to the reader how they are built up from more elementary pieces.
