---
title: "Interfaces vs. Abstract Classes"
weight: 50
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/InterfacesVsAbstractClasses.md#interfaces-vs-abstract-classes"
---

Although interfaces and abstract classes share some properties,
they are not equivalent and you should not treat one
as an alternative for the other.

Interfaces are there to share definitions.
They specify how things are supposed to interact,
without imposing any expectations
what the implementation should look like.

Abstract classes are there to share implementations.
They also specify interaction,
but in a way that already plots a path how to implement it,
probably even assisting that implementation with code.

Instead of asking _"should I use an interface or an abstract class?"_,
usually the clean way will be to state that _"I will use an interface"_,
followed by the question _"should I use an abstract class to implement it?"_.
