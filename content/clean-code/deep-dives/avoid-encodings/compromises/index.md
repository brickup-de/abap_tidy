---
title: "Compromises"
weight: 50
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/AvoidEncodings.md#compromises"
---

The only prefix that ABAP forces you to use is your application's namespace,
to avoid conflicts with objects from other teams in the global dictionary, where every thing needs a unique name.

If this rule is too hard for you, consider a compromise:  
Avoid encodings in local contexts (within a method body, method parameters, local classes, etc.),
and apply them only to global objects that are stored in the same global Dictionary namespace.

We agree that following this suggestion will work out only if the code is already _clean_ in some other aspects,
especially short methods and good method and variable names.
While prefixes needlessly complicate a clean code with extra three characters in names,
they may be your only remaining lifeline in a thousand-line legacy function with cryptic variable names.
