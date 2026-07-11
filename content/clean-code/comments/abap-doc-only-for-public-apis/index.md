---
title: "ABAP Doc only for public APIs"
weight: 130
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#abap-doc-only-for-public-apis"
---

Write ABAP Doc to document public APIs,
meaning APIs that are intended for developers
in other teams or applications.
Don't write ABAP Doc for internal stuff.

ABAP Doc suffers from the same weaknesses as all comments,
that is, it outdates quickly and then becomes misleading.
As a consequence, you should employ it only where it makes sense,
not enforce writing ABAP Doc for each and everything.

> Read more in _Chapter 4: Good Comments: Javadocs in Public APIs_ and _Chapter 4: Bad Comments:
> Javadocs in Nonpublic Code_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
