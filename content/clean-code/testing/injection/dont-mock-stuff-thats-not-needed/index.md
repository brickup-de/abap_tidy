---
title: "Don't mock stuff that's not needed"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-mock-stuff-thats-not-needed"
---

```ABAP
cut = NEW /clean/class_under_test( db_reader = db_reader
                                   config    = VALUE #( )
                                   writer    = VALUE #( ) ).
```

Define your givens as precisely as possible: don't set data that your test doesn't need,
and don't mock objects that are never called.
These things distract the reader from what's really going on.

```ABAP
" anti-pattern
cut = NEW /dirty/class_under_test( db_reader = db_reader
                                   config    = config
                                   writer    = writer ).
```

There are also cases where it's not necessary to mock something at all -
this is usually the case with data structures and data containers.
For example, your unit tests may well work with the production version of a `transient_log`
because it only stores data without any side effects.
