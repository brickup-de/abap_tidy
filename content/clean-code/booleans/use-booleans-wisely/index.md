---
title: "Use Booleans wisely"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-booleans-wisely"
---

We often encounter cases where Booleans seem to be a natural choice

```ABAP
" anti-pattern
is_archived = abap_true.
```

until a change of viewpoint suggests
we should have chosen an enumeration

```ABAP
archiving_status = /clean/archivation_status=>archiving_in_process.
```

Generally, Booleans are a bad choice
to distinguish types of things
because you will nearly always encounter cases
that are not exclusively one or the other

```ABAP
assert_true( xsdbool( document->is_archived( ) = abap_true AND
                      document->is_partially_archived( ) = abap_true ) ).
```

[Split method instead of Boolean input parameter](/clean-code/methods/parameter-types/split-method-instead-of-boolean-input-parameter/)
moreover explains why you should always challenge Boolean parameters.
