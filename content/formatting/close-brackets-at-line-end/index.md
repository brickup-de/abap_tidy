---
title: "Close brackets at line end"
weight: 110
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#close-brackets-at-line-end"
---

```ABAP
modify->update( node           = if_fra_alert_c=>node-item
                key            = item->key
                data           = item
                changed_fields = changed_fields ).
```

instead of the needlessly longer

```ABAP
" anti-pattern
modify->update( node           = if_fra_alert_c=>node-item
                key            = item->key
                data           = item
                changed_fields = changed_fields
).
```
