---
title: "Abstract"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/AvoidEncodings.md#abstract"
---

We encourage you to get rid of _all_ encoding prefixes.

```ABAP
METHOD add_two_numbers.
  result = a + b.
ENDMETHOD.
```

instead of the needlessly longer

```ABAP
" anti-pattern
METHOD add_two_numbers.
  rv_result = iv_a + iv_b.
ENDMETHOD.
```

> Read more in _Chapter 2: Meaningful Names: Avoid Encodings_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
> The examples in this style guide are written without prefixes to demonstrate the value.
>
> This section contradicts the sections [_Names of Repository Objects_](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/index.htm?file=abennames_repos_obj_guidl.htm)
> and [_Program-Internal Names_](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/index.htm?file=abenprog_intern_names_guidl.htm)
> of the ABAP Programming Guidelines which recommend to use prefixes.
> We think that avoiding prefixes is the more modern and readable variant and that the guideline should be adjusted.
>
> Prefixing is one of the most controversially discussed topics in ABAP.
> [[1]](https://blogs.sap.com/2009/08/30/nomen-est-omen-abap-naming-conventions/)
> [[2]](https://blogs.sap.com/2016/02/05/fanning-the-flames-prefixing-variableattribute-names/)
> [[3]](https://blogs.sap.com/2018/04/30/are-30-characters-enough-to-make-your-code-better/)
> [[4]](https://blogs.sap.com/2018/05/11/all-your-abap-prefixes-are-belong-to-us/)
