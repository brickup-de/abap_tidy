---
title: "Align parameters"
weight: 160
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#align-parameters"
---

```ABAP
modify->update( node           = if_fra_alert_c=>node-item
                key            = item->key
                data           = item
                changed_fields = changed_fields ).
```

Ragged margins make it hard to see where the parameter ends and its value begins:

```ABAP
" anti-pattern
modify->update( node = if_fra_alert_c=>node-item
                key = item->key
                data = item
                changed_fields = changed_fields ).
```

> This is on the other side the best pattern if you want to avoid the formatting to be broken by a name length change.
