---
title: "Don't mock stuff that's not needed"
linkTitle: "Don't mock stuff needlessly"
weight: 90
params:
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
