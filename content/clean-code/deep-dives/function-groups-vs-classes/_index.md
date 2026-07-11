---
title: "Function Groups vs. Classes"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/FunctionGroupsVsClasses.md#function-groups-vs-classes"
---

New clean coders routinely ask for clarifying
the advantage of classes over function groups.

Think of a function group as a `global abstract final class`,
with functions, form routines, and global variables
as `static public` members.
 
This yields the following comparison:
