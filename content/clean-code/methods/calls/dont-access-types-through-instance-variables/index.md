---
title: "Don't access types through instance variables"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-access-types-through-instance-variables"
---

When using a data type that is defined in a class or interface, access the type definition via the class/interface and not via an instance of the class/interface. 

```ABAP
CLASS lcl DEFINITION.
  PUBLIC SECTION.
    TYPES foo TYPE i.
ENDCLASS.
CLASS lcl IMPLEMENTATION.
ENDCLASS.

INTERFACE lif.
  TYPES blah TYPE lcl=>foo.  
ENDINTERFACE.
```

Using the instance for the data type would be confusing, as it suggests that the type is instance specific. 

```ABAP
" anti-pattern
CLASS lcl DEFINITION.
  PUBLIC SECTION.
    TYPES foo TYPE i.
ENDCLASS.
CLASS lcl IMPLEMENTATION.
ENDCLASS.

INTERFACE lif.
  DATA(ref) = new lcl( ).
  TYPES blah TYPE ref->foo.
ENDINTERFACE.
```
