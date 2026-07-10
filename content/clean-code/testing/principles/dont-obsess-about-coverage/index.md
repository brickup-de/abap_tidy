---
title: "Don't obsess about coverage"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-obsess-about-coverage"
---

Code coverage is there to help you find code you forgot to test, not to meet some random KPI:

Don't make up tests without or with dummy asserts just to reach the coverage.
Better leave things untested to make transparent that you cannot safely refactor them.
You can have < 100% coverage and still have perfect tests.
There are cases - such as IFs in the constructor to insert test doubles -
that may make it unpractical to reach 100%.
Good tests tend to cover the same statement multiple times, for different branches and conditions.
They will in fact have imaginary > 100% coverage.
