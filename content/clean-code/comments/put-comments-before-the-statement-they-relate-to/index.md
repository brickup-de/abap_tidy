---
title: "Put comments before the statement they relate to"
weight: 70
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#put-comments-before-the-statement-they-relate-to"
---

```ABAP
" delegate pattern
output = calculate_result( input ).
```

Clearer than

```ABAP
" anti-pattern
output = calculate_result( input ).
" delegate pattern
```

And less invasive than

```ABAP
output = calculate_result( input ).  " delegate pattern
```
