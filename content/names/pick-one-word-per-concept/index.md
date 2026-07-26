---
title: "Pick one word per concept"
weight: 100
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#pick-one-word-per-concept"
---

```ABAP
METHODS read_this.
METHODS read_that.
METHODS read_those.
```

Choose a term for a concept and stick to it; don't mix in other synonyms.
Synonyms will make the reader waste time on finding a difference that's not there.

```ABAP
" anti-pattern
METHODS read_this.
METHODS retrieve_that.
METHODS query_those.
```

> Read more in _Chapter 2: Meaningful Names: Pick One Word per Concept_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/)
