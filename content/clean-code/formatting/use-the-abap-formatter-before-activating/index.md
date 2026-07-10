---
title: "Use the ABAP Formatter before activating"
weight: 30
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-the-abap-formatter-before-activating"
---

Apply the ABAP Formatter - Shift+F1 in SE80, SE24, and ADT - before activating an object.  
Note: ABAP Formatter is known as Pretty Printer in SAP GUI.

If you modify a larger unformatted legacy code base,
you may want to apply the ABAP Formatter only to selected lines
to avoid huge change lists and transport dependencies.
Consider formatting the complete development object
in a separate Transport Request or Note.

> Read more in _Chapter 5: Formatting: Team Rules_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
