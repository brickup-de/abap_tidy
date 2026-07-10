---
title: "Don't add features to production code that are only intended for use during automated testing"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-add-features-to-production-code-that-are-only-intended-for-use-during-automated-testing"
---

For reasons already described under [Test Seams](/clean-code/testing/injection/use-test-seams-as-temporary-workaround/), adding anything to production code that is solely intended for use during automated tests should be avoided.
```ABAP
" anti-pattern
IF is_unit_test_running = abap_true.
  "some logic here that runs only during unit tests
ENDIF.  
```
Note that test features intended to be executed by an end user, e.g. simulated posting or running a report in test mode, form part of the application domain and remain a valid use case.
