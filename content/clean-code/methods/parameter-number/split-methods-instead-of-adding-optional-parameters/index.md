---
title: "Split methods instead of adding OPTIONAL parameters"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#split-methods-instead-of-adding-optional-parameters"
---

```ABAP
METHODS do_one_thing IMPORTING what_i_need TYPE string.
METHODS do_another_thing IMPORTING something_else TYPE i.
```

to achieve the desired semantic as ABAP does not support [overloading](https://en.wikipedia.org/wiki/Function_overloading).

```ABAP
" anti-pattern
METHODS do_one_or_the_other
  IMPORTING
    what_i_need    TYPE string OPTIONAL
    something_else TYPE i OPTIONAL.
```

Optional parameters confuse callers:

- Which ones are really required?
- Which combinations are valid?
- Which ones exclude each other?

Multiple methods with specific parameters for the use case avoid this confusion by giving clear guidance which parameter combinations are valid and expected.
