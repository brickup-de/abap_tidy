---
title: "Avoid obscuring built-in functions"
weight: 130
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#avoid-obscuring-built-in-functions"
---

Within a class, a built-in function is always obscured by methods of the class if they have the same name, regardless of the number and type of arguments in the function. The function is also obscured regardless of the number and type of method parameters. Built-in functions are, for instance, `condense( )`, `lines( )`, `line_exists( )`, `strlen( )`, etc. 

```ABAP
"anti-pattern
METHODS lines RETURNING VALUE(result) TYPE i.    
METHODS line_exists RETURNING VALUE(result) TYPE i.  
```

```ABAP
"anti-pattern 
CLASS-METHODS condense RETURNING VALUE(result) TYPE i.   
CLASS-METHODS strlen RETURNING VALUE(result) TYPE i.  
```

> Read More in [Built-In Functions - Obscuring with Methods](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-us/abenbuilt_in_functions_syntax.htm).
