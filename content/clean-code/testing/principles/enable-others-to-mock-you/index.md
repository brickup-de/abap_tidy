---
title: "Enable others to mock you"
weight: 10
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#enable-others-to-mock-you"
---

If you write code to be consumed by others, enable them to write unit tests for their own code,
for example by adding interfaces in all outward-facing places,
providing helpful test doubles that facilitate integration tests,
or applying dependency inversion to enable them to substitute the configuration with a test config.
