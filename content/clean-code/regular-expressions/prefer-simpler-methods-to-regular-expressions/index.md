---
title: "Prefer simpler methods to regular expressions"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#prefer-simpler-methods-to-regular-expressions"
---

```ABAP
IF input IS NOT INITIAL.
" IF matches( val = input  regex = '.+' ).

WHILE contains( val = input  sub = 'abc' ).
" WHILE contains( val = input  regex = 'abc' ).
```

Regular expressions become hard to understand very quickly.
Simple cases are usually easier without them.

Regular expressions also usually consume more memory and processing time
because they need to be parsed into an expression tree and compiled at runtime into an executable matcher.
Simple solutions may do with a straight-forward loop and a temporary variable.
