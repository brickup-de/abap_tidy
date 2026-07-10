---
title: "Don't sub-class to mock methods"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-sub-class-to-mock-methods"
---

Don't sub-class and overwrite methods to mock them in your unit tests.
Although this works, it is fragile because the tests break easily when refactoring the code.
It also enables real consumers to inherit your class,
which [may hit you unprepared when not explicitly designing for it](/clean-code/classes/scope/final-if-not-designed-for-inheritance/).

```ABAP
" anti-pattern
CLASS unit_tests DEFINITION INHERITING FROM /dirty/real_class FOR TESTING [...].
  PROTECTED SECTION.
    METHODS needs_to_be_mocked REDEFINITION.
```

To get legacy code under test,
[resort to test seams instead](/clean-code/testing/injection/use-test-seams-as-temporary-workaround/).
They are just as fragile but still the cleaner way because they at least don't change the class's behavior in production,
as would happen when enabling inheritance by removing a previous `FINAL` flag or by changing method scope from `PRIVATE` to `PROTECTED`.

When writing new code, take this testability issue into account directly when designing the class,
and find a different, better way.
Common best practices include [resorting to other test tools](/clean-code/testing/injection/exploit-the-test-tools/)
and extracting the problem method to a separate class with its own interface.

> A more specific variant of
> [Don't change the production code to make the code testable](/clean-code/testing/injection/dont-add-features-to-production-code-that-are-only-intended-for-use-during-automated-testing/).
