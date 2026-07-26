---
title: "Don't duplicate message texts as comments"
weight: 120
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-duplicate-message-texts-as-comments"
---

```ABAP
" anti-pattern
" alert category not filled
MESSAGE e003 INTO dummy.
```

Messages change independently from your code,
and nobody will remember adjusting the comment,
such that it will outdate and even become misleading quickly
and without anybody noticing.

The modern IDEs give you easy ways to see the text behind a message,
for example in the ABAP Development Tools,
mark the message ID and press F2.

If you want it more explicit,
consider extracting the message to a method of its own.

```ABAP
METHOD create_alert_not_found_message.
  MESSAGE e003 INTO dummy.
ENDMETHOD.
```
