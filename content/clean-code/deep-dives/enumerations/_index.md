---
title: "Enumerations"
weight: 20
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#enumerations"
---

ABAP did not support enumerations as natively and completely as other programming languages before release 7.51.

ABAPers therefore were forced to think up their own solutions
and came up with a set of [patterns](/clean-code/deep-dives/enumerations/patterns/) that can be
found in the majority of today's object-oriented ABAP code.

**Starting with release 7.51 native enumerated types are available and should be preferred where applicable.**
They offer [compatibility](/clean-code/deep-dives/enumerations/native-enumerations/compatibility/) features to easily refactor legacy enumeration patterns.
When deciding against native enumerations or wanting to design one of your own, consider the [guidelines](/clean-code/deep-dives/enumerations/guidelines/).
