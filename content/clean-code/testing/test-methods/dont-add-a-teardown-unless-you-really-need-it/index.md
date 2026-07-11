---
title: "Don't add a TEARDOWN unless you really need it"
weight: 10
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#dont-add-a-teardown-unless-you-really-need-it"
---

`teardown` methods are usually only needed to clear up database entries
or other external resources in integration tests.

Resetting members of the test class, esp. `cut` and the used test doubles, is superfluous;
they are overwritten by the `setup` method before the next test method is started.
