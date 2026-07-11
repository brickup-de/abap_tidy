---
title: "Prefer functional to procedural calls"
linkTitle: "Prefer functional"
weight: 30
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-functional-to-procedural-calls"
---

```ABAP
modify->update( node           = /clean/my_bo_c=>node-item
                key            = item->key
                data           = item
                changed_fields = changed_fields ).
```

instead of the needlessly longer

```ABAP
" anti-pattern
CALL METHOD modify->update
  EXPORTING
    node           = /dirty/my_bo_c=>node-item
    key            = item->key
    data           = item
    changed_fields = changed_fields.
```

If dynamic typing forbids functional calls, resort to the procedural style

```ABAP
CALL METHOD modify->(method_name)
  EXPORTING
    node           = /clean/my_bo_c=>node-item
    key            = item->key
    data           = item
    changed_fields = changed_fields.
```

Many of the related rules are just more specific variations of this advice.
