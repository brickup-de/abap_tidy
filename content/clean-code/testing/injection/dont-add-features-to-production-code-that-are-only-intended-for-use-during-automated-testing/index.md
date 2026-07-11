---
title: "Don't add features to production code that are only intended for use during automated testing"
linkTitle: "Don't add test-only features to production"
weight: 70
params:
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
