---
title: "Use ` to define literals"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-to-define-literals"
---

```ABAP
CONSTANTS some_constant TYPE string VALUE `ABC`.
DATA(some_string) = `ABC`.  " --> TYPE string
```

Refrain from using `'`, as it adds a superfluous type conversion and confuses the reader
whether he's dealing with a `CHAR` or `STRING`:

```ABAP
" anti-pattern
DATA some_string TYPE string.
some_string = 'ABC'.
```

`|` is generally okay, but cannot be used for `CONSTANTS` and adds needless overhead when specifying a fixed value:

```ABAP
" anti-pattern
DATA(some_string) = |ABC|.
```
