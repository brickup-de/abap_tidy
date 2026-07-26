---
title: "Choose the right targets for your loops"
linkTitle: "Choose the right loop target"
weight: 50
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#choose-the-right-targets-for-your-loops"
---

There are three possible targets for an ABAP loop: A field symbol (`LOOP AT table ASSIGNING FIELD-SYMBOL(<line>).`), a reference variable (`LOOP AT table REFERENCE INTO DATA(line).`) or a plain data object (`LOOP AT table INTO DATA(line).`). Each of these have different intended use cases:

 - Field symbols when you want to read or manipulate the data being iterated over. 
 - Data references when you need to access these references outside of the current loop, e.g. pass them into methods whose input parameters are references or keep references to the data around after the loop has finished.
 - Data objects when you need a copy of the data itself or when the line type of the table is already a reference.

Note that data references can be used to read or manipulate the data as well. That is, almost all instances of field symbols as loop targets can be replaced by references as loop targets.

For consistency with the general pattern of object oriented ABAP using references you may wish to use references as loop targets whenever possible. On the other hand, when you want to access the entire value of the line type, using data references introduces additional dereferencing operations that are unnecessary when using field symbols. Compare

```ABAP
LOOP AT table ASSIGNING FIELD-SYMBOL(<line>).
  obj->do_something( <line> ).
ENDLOOP.
```

to

```ABAP
LOOP AT table REFERENCE INTO DATA(line).
  obj->do_something( line->* ).
ENDLOOP.
```

Additionally, data access via field symbols is slightly faster than data access via references. This is only noticable when loops make up a significant part of the runtime of the program and is often not relevant, e.g. when database operations or other input/output processes dominate the runtime.

For these reasons, there are two possible consistent styles depending on the specific application context:

 - If the context mostly uses objects and references otherwise, and if small performance hits in loops are not generally relevant, use references instead of field symbols as loop targets whenever possible.
 - If the context performs a lot of manipulation of plain data and not references or objects, or if small performance hits in loops are generally relevant, use field symbols to read and manipulate data in loops.
