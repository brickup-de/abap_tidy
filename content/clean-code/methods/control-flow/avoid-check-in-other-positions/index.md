---
title: "Avoid CHECK in other positions"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#avoid-check-in-other-positions"
---

Do not use `CHECK` outside of the initialization section of a method.
The statement behaves differently in different positions and may lead to unclear, unexpected effects.

For example,
[`CHECK` in a `LOOP` ends the current iteration and proceeds with the next one](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abapcheck_loop.htm);
people might accidentally expect it to end the method or exit the loop.
Prefer using an `IF` statement in combination with `CONTINUE` instead, since `CONTINUE` only can be used in loops.

> Based on the [section _Exiting Procedures_ in the ABAP Programming Guidelines](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/index.htm?file=abenexit_procedure_guidl.htm).
> Note that this contradicts the [keyword reference for `CHECK` in loops](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/abapcheck_loop.htm).
