---
title: "Patterns"
weight: 20
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#patterns"
---

> [Enumerations](/clean-code/deep-dives/enumerations/) > [This section](/clean-code/deep-dives/enumerations/patterns/)

If native `ENUM` cannot be used we recommend either
the **[constant pattern](/clean-code/deep-dives/enumerations/patterns/constant-pattern/)**
or the **[object pattern](/clean-code/deep-dives/enumerations/patterns/object-pattern/)**
because they combine most advantages
and can be generally considered clean.

The widely used [interface pattern](/clean-code/deep-dives/enumerations/patterns/interface-pattern/)
is also acceptable, but has some slight drawbacks.

Think twice before resorting to the
[collection pattern](/clean-code/deep-dives/enumerations/patterns/collection-pattern/).
Although it has become widely spread through BOPF,
and can be quite convenient in some scenarios,
it harbors the danger of degrading into a mess.
