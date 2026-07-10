---
title: "Copy fields with matching names"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#copy-fields-with-matching-names"
---

Copy fields with matching names from one data type to another with `corresponding #( )`.

```ABAP
target_structure = CORRESPONDING #( source_structure ).
```

Old style:

```ABAP
MOVE-CORRESPONDING source_structure TO target_structure.
```

> Caution: The two statements differ in behavior.
> The `CORRESPONDING( )` statement is a constructor statement, meaning all fields in the `target_structure` are initialized before the corresponding `source_structure` values are copied to the `target_sructure`
> The `MOVE-CORRESPONDING` statement in contrast leaves the content of the not matching fields in the `target_structure` untouched.
