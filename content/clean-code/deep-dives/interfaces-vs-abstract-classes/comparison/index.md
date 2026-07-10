---
title: "Comparison"
weight: 50
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/InterfacesVsAbstractClasses.md#comparison"
---

- An abstract class needs more code
because you always have to provide an `IMPLEMENTATION`,
even if it is completely empty.

- An abstract class can reduce the amount of code needed by providing 
a default behavior in a non-abstract method. If such a method 
would have been part of the interface, it would have to be 
implemented separately for each class implementing the interface.

- A class can implement multiple interfaces,
but can inherit only one interface-like abstract class. Remember to 
[favor composition over inheritance](/clean-code/clean-abap-md-prefer-composition-to-inheritance/), though.

- Inheriting from the interface-like abstract class
disables inheriting from other classes,
preventing the sub-class from exploiting inheritance for other aspects.

- Interfaces have no optional methods,
such that adding a method requires you
to adjust all implementations.

- Interfaces provide only `PUBLIC` components,
while abstract classes can provide `PROTECTED` parts as well,
sharing something with the sub-class but not with the rest of the world.

- Sub-class constructors must call `super->constructor( )`,
even if the abstract class does not have a constructor.

- The abstract class has power over the sub-class's instantiation behavior,
being able to suppress instantiation completely with `CREATE PRIVATE`.

- The abstract class has power over the sub-class's code,
being able to add members and constructor code that may
simplify but also interfere with or even break the sub-class's code.

- Unit testing is easier with interfaces,
because they allow plugging in any kind of test double.
Interface-like abstract classes require the test double
to inherit the abstract class, probably involuntarily
running code included in it, esp. its constructor.
