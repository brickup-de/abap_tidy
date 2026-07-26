---
title: "Comment with \", not with *"
weight: 60
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#comment-with--not-with-"
---

Quote comments indent along with the statements they comment

```ABAP
METHOD do_it.
  IF input IS NOT INITIAL.
    " delegate pattern
    output = calculate_result( input ).
  ENDIF.
ENDMETHOD.
```

Asterisked comments tend to indent to weird places

```ABAP
" anti-pattern
METHOD do_it.
  IF input IS NOT INITIAL.
* delegate pattern
    output = calculate_result( input ).
  ENDIF.
ENDMETHOD.
```
