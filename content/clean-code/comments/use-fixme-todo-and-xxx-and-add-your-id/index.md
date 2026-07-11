---
title: "Use FIXME, TODO, and XXX and add your ID"
weight: 100
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-fixme-todo-and-xxx-and-add-your-id"
---

```ABAP
METHOD do_something.
  " XXX FH delete this method - it does nothing
ENDMETHOD.
```

- `FIXME` points to errors that are too small or too much in-the-making for internal incidents.
- `TODO`s are places where you want to complete something in the near(!) future.
- `XXX` marks code that works but could be better.

When you enter such a comment, add your nick, initials, or user to enable your co-developers to contact you
and ask questions if the comment is unclear.
