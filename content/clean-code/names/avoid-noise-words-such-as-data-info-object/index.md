---
title: "Avoid noise words such as \"data\", \"info\", \"object\""
linkTitle: "Avoid noise words"
weight: 90
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#avoid-noise-words-such-as-data-info-object"
---

Omit noise words

```ABAP
account  " instead of account_data
alert    " instead of alert_object
```

or replace them with something specific that really adds value

```ABAP
user_preferences          " instead of user_info
response_time_in_seconds  " instead of response_time_variable
```

> Read more in _Chapter 2: Meaningful Names: Make Meaningful Distinctions_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/)
