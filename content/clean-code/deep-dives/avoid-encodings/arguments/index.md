---
title: "Arguments"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/AvoidEncodings.md#arguments"
---

Before you disagree, consider these:

- ABAP's 30 character limitation makes it hard enough to squeeze meaningful names
  into the available space without wasting another 3-4 characters for needless encodings.

- The disputes that arise over prefixes are not worth the effort:
  whether your constant starts with `sc_` or `cv_` does not really influence readability.

- Squeezing the at least five dimensions of variables
  (kind, direction, scope, type, mutability),
  into usually no more than two character prefixes
  leads to pointless conflicts.
  
- Different team styles create confusion:
  is `lr_` an object reference or a range table?
  You'll stumble over this in code that connects different things,
  for example your determinations within BOPF.

- Prefixes can be misleading.
  For example, despite their names,
  the "importing data" `id_business_partner`
  has nothing to do with the business partner's ID,
  and the "large object string" `lost_file_content`
  is not lost at all.

- Changes create needless work: turning a table from `STANDARD` to `SORTED` shouldn't require you
  to rename all variables from `lt_` to `lts_`.
  
- Prefixing doesn't make it easier to tell global from local things.
  If you fill a `gt_sum` from an `lt_sum`, both are still only sums and it's not clear what distinguishes the two.
  The better idea is to fill a `total_sum` from a `partial_sum`, or an `overall_result` from an `intermediate_result`.
  The name confusion described in
  [section _Program-Internal Names_ in the ABAP Programming Guidelines](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/index.htm?file=abenprog_intern_names_guidl.htm)
  should thus be solved otherwise.

- Prefixing doesn't make it easier to recognize data types.
  For example, most Hungarian ABAP encodings
  distinguish variables from structures and tables,
  but don't reflect the way more important differentiation
  between floating point and packed numbers.

- If you follow Clean Code, your methods will become so short (3-5 statements)
  that prefixing is no longer necessary to tell importing from exporting parameters and local from global variables.

- The ABAP foundation doesn't prefix anymore,
  for example you won't find importing/exporting prefixes
  on the method parameters in `cl_abap_math`.

- Other languages like Java use absolutely no prefixes,
  and still Java code is perfectly readable.
