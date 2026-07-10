---
title: "RETURN, EXPORT, or CHANGE exactly one parameter"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#return-export-or-change-exactly-one-parameter"
---

A good method does _one thing_, and that should be reflected by the method also returning exactly one thing.
If the output parameters of your method do _not_ form a logical entity,
your method does more than one thing and you should split it.

There are cases where the output is a logical entity that consists of multiple things.
These are easiest represented by returning a structure or object:

```ABAP
TYPES:
  BEGIN OF check_result,
    result      TYPE result_type,
    failed_keys TYPE /bobf/t_frw_key,
    messages    TYPE /bobf/t_frw_message,
  END OF check_result.

METHODS check_business_partners
  IMPORTING
    business_partners TYPE business_partners
  RETURNING
    VALUE(result)     TYPE check_result.
```

instead of

```ABAP
" anti-pattern
METHODS check_business_partners
  IMPORTING
    business_partners TYPE business_partners
  EXPORTING
    result            TYPE result_type
    failed_keys       TYPE /bobf/t_frw_key
    messages          TYPE /bobf/t_frw_message.
```

Especially in comparison to multiple EXPORTING parameters, this allows people to use the functional call style,
spares you having to think about `IS SUPPLIED` and saves people from accidentally forgetting
to retrieve a vital `ERROR_OCCURRED` information.

Instead of multiple optional output parameters, consider splitting the method according to meaningful call patterns:

```ABAP
TYPES:
  BEGIN OF check_result,
    result      TYPE result_type,
    failed_keys TYPE /bobf/t_frw_key,
    messages    TYPE /bobf/t_frw_message,
  END OF check_result.

METHODS check
  IMPORTING
    business_partners TYPE business_partners
  RETURNING
    VALUE(result)     TYPE result_type.

METHODS check_and_report
  IMPORTING
    business_partners TYPE business_partners
  RETURNING
    VALUE(result)     TYPE check_result.
```
