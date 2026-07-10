---
title: "Use snake_case"
weight: 50
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-snakecase"
---

ABAP is case insensitive which is why we recommend following the convention to use `snake_case` consistently.

There's a character limit for names, e.g. 30 characters for methods. When you reach the maximum length of an object, don't fall back to using `flatcase` or `UPPERCASE`. Try to conscientiously use abbreviations instead (see [Use same abbreviations everywhere](/clean-code/names/use-same-abbreviations-everywhere/)).

```ABAP
" a variable which contains the maximum reponse time measured in milliseconds
DATA max_response_time_in_millisec TYPE i.
```

is better than

```ABAP
" anti-pattern
DATA maxresponsetimeinmilliseconds TYPE i.
```
