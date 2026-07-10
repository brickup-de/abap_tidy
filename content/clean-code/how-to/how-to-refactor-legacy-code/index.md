---
title: "How to Refactor Legacy Code"
weight: 20
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#how-to-refactor-legacy-code"
---

The topics [Booleans](/clean-code/booleans/), [Conditions](/clean-code/conditions/), [Ifs](/clean-code/ifs/),
and [Methods](/clean-code/methods/) are most rewarding if you are working on a legacy project
with tons of code that you cannot or do not want to change
because they can be applied to new code without conflicts.

The topic [Names](/clean-code/names/) is very demanding for legacy projects,
as it may introduce a breach between old and new code,
up to a degree where sections like
[Avoid encodings, esp. Hungarian notation and prefixes](/clean-code/names/avoid-encodings-esp-hungarian-notation-and-prefixes/)
are better ignored.

Try not to mix different development styles within the same
development object when carrying out a refactoring. If the
legacy code contains only up-front declarations, and a complete
refactoring into using inline declarations is not feasible, it
is probably better to stick with the legacy style rather than
mixing the two styles. There are several similar situations
where mixing styles could cause confusion, for example:

- Mixing `REF TO` and `FIELD-SYMBOL` when looping.
- Mixing `NEW` and `CREATE OBJECT` when calling a `CONSTRUCTOR`.
- Mixing `RETURNING` and `EXPORTING` in the method signatures of
methods only returning / exporting one parameter.

We observed good results with a four-step plan for refactoring:

1. Get the team aboard. Communicate and explain the new style,
and get everybody on the project team to agree to it.
You don't need to commit all guidelines at once, just start
with an undisputed small subset and evolve from there.

2. Follow the _boy scout rule_ to your daily work routine:
_always leave the code you edit a little cleaner than you found it_.
Don't obsess with this by sinking hours into "cleaning the campsite",
just spend a couple of minutes extra and observe how the
improvements accumulate over time.

3. Build _clean islands_: from time to time, pick a small object or component and
try to make it clean in all aspects. These islands demonstrate the benefit
of what you're doing and form solidly tested home bases for further refactoring.

4. Talk about it. No matter whether you set up old-school [Fagan code reviews](https://en.wikipedia.org/wiki/Fagan_inspection),
hold info sessions, or form discussion boards in your favorite chat tool:
you will need to talk about your experiences and learnings, to enable the
team to grow a common understanding.
