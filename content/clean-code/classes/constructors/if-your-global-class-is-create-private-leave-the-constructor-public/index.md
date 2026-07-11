---
title: "If your global class is CREATE PRIVATE, leave the CONSTRUCTOR public"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#if-your-global-class-is-create-private-leave-the-constructor-public"
---

```ABAP
CLASS /clean/some_api DEFINITION PUBLIC FINAL CREATE PRIVATE.
  PUBLIC SECTION.
    METHODS constructor.
```

We agree that this contradicts itself.
However, according to the article
[_Instance Constructor_ of the ABAP Help](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abeninstance_constructor_guidl.htm),
specifying the `CONSTRUCTOR` in the `PUBLIC SECTION` is required to guarantee correct compilation and syntax validation.

This applies only to global classes.
In local classes, make the constructor private, as it should be.
