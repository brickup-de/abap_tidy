---
title: "Use plural"
weight: 30
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-plural"
---

There is a legacy practice at SAP to name tables of things in singular,
for example `country` for a "table of countries".
Common tendency in the outside world is to use the plural for lists of things.
We therefore recommend to prefer `countries` instead.

> This advice primarily targets things like variables and properties.
> For development objects, there may be competing patterns
> that also make sense, for example the widely used convention
> to name database tables ("transparent tables") in singular.

> Read more in _Chapter 2: Meaningful Names: Use Intention-Revealing Names_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
