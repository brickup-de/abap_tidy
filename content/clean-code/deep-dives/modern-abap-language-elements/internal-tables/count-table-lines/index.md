---
title: "Count table lines"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/ModernABAPLanguageElements.md#count-table-lines"
---

Count the number of lines of an internal table with
[`lines( )`](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/abendescriptive_functions_table.htm).

```ABAP
DATA(number_of_lines) = lines( accounts ).
```

Old style:

```ABAP
DATA number_of_lines TYPE i.
DESCRIBE TABLE accounts LINES number_of_lines.
```
