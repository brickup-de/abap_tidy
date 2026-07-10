---
title: "Combination"
weight: 50
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/InterfacesVsAbstractClasses.md#combination"
---

Instead of using abstract classes as alternative to interfaces,
you should use both in combination to decouple dependencies.

```ABAP
INTERFACE /clean/blog_post.
  METHODS publish.
ENDINTERFACE.
```

```ABAP
CLASS /clean/formatted_blog_post DEFINITION PUBLIC ABSTRACT CREATE PROTECTED.
  PUBLIC SECTION.
    INTERFACES /clean/blog_post.
ENDCLASS.

CLASS /clean/formatted_blog_post IMPLEMENTATION.

  METHOD /clean/blog_post~publish.
    " default implementation
    " sub-classes can use it
    " or override the method with something else
  ENDMETHOD.
  
ENDCLASS.
```

![](InterfacesVsAbstractClasses-Combined.png)

> **Class diagram.**
The interface `BlogPost` specifies the "contract"
that all blog posts will fulfill.
The developers decided to use an inheritance scheme to implement
different "flavors" of blog posts,
using an abstract class `FormattedBlogPost` with two sub-classes
`MarkdownBlogPost` and `HTMLBlogPost`.
