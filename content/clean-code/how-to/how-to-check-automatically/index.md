---
title: "How to Check Automatically"
weight: 30
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#how-to-check-automatically"
---

[code pal for ABAP](https://github.com/SAP/code-pal-for-abap)
provides a comprehensive suite of automatic checks for Clean ABAP.

ABAP Test Cockpit, Code Inspector, Extended Check, and Checkman provide
some checks that may help you find certain issues.

[abapOpenChecks](https://github.com/larshp/abapOpenChecks),
an Open Source collection of Code Inspector checks,
also covers some of the described anti-patterns.

[abaplint](https://github.com/abaplint/abaplint) is an open source reimplementation of the ABAP parser. It works without a SAP system and is meant to be used on code serialized using abapGit. It offers multiple integrations (GitHub Actions, Jenkins, text editors...), covers some of the antipatterns and can also be used to check formatting and code conventions.
