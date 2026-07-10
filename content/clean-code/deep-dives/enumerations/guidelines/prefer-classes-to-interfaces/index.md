---
title: "Prefer classes to interfaces"
weight: 10
date: 2026-07-05
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/sub-sections/Enumerations.md#prefer-classes-to-interfaces"
---

> [Enumerations](/clean-code/deep-dives/enumerations/enumerations/) > [Guidelines](/clean-code/deep-dives/enumerations/guidelines/) > [This section](/clean-code/deep-dives/enumerations/guidelines/prefer-classes-to-interfaces/)

```ABAP
CLASS /clean/message_severity DEFINITION PUBLIC ABSTRACT FINAL.
  PUBLIC SECTION.
    CONSTANTS:
      warning TYPE symsgty VALUE 'W',
      error   TYPE symsgty VALUE 'E'.
ENDCLASS.
```

Classes allow adding supportive methods,
such as the often-encountered
`is_valid`, `equals`, `contains`, and `to_string` methods,
or enumeration-specific ones such as `is_more_severe_than`.

They also provide a natural place for unit tests,
especially if you added supportive methods,
but also for common cases such as
`in_sync_with_domain_fixed_vals`.
<details>
  <summary>The local test class for the constant pattern can look like this:</summary>
  
```ABAP
CLASS ltcl_constant_pattern DEFINITION CREATE PRIVATE
 FOR TESTING
 RISK LEVEL HARMLESS
 DURATION SHORT.

  PUBLIC SECTION.
  PROTECTED SECTION.
  PRIVATE SECTION.
    CONSTANTS class_name TYPE classname VALUE '/CLEAN/MESSAGE_SEVERITY'.
    CONSTANTS domain_name TYPE domname  VALUE 'DOM_MSG_SEVERITY'.
    DATA domain_values TYPE STANDARD TABLE OF dd07v.
    DATA constants_of_enum_class TYPE abap_attrdescr_tab.

    METHODS setup.
    METHODS all_values_as_constant FOR TESTING.
    METHODS all_constants_in_domain FOR TESTING.
ENDCLASS.

CLASS ltcl_constant_pattern IMPLEMENTATION.
  METHOD setup.
    CALL FUNCTION 'DD_DOMVALUES_GET'
      EXPORTING
        domname   = domain_name
      TABLES
        dd07v_tab = domain_values
      EXCEPTIONS
        OTHERS    = 1.
    ASSERT sy-subrc = 0.

    DATA class_descr TYPE REF TO cl_abap_classdescr.
    class_descr ?= cl_abap_typedescr=>describe_by_name( class_name ).

    constants_of_enum_class = class_descr->attributes.
  ENDMETHOD.

  METHOD all_constants_in_domain.
    LOOP AT constants_of_enum_class INTO DATA(component).
    
      ASSIGN (class_name)=>(component-name) TO FIELD-SYMBOL(<value>).
      ASSERT sy-subrc = 0.
      
      IF NOT line_exists( domain_values[ domvalue_l = <value> ] ).
        cl_abap_unit_assert=>fail( |Component { component-name } not found in domain fix values| ).
      ENDIF.
    ENDLOOP.

  ENDMETHOD.

  METHOD all_values_as_constant.
    DATA value_found TYPE abap_bool.

    LOOP AT domain_values INTO DATA(domain_value).

      CLEAR value_found.
      LOOP AT constants_of_enum_class INTO DATA(component).

        ASSIGN (class_name)=>(component-name) TO FIELD-SYMBOL(<value>).
        ASSERT sy-subrc = 0.

        IF  domain_value-domvalue_l = <value>.
          value_found = abap_true.
          EXIT.
        ENDIF.
      ENDLOOP.
      IF value_found = abap_false.
        cl_abap_unit_assert=>fail( |Domainvalue { domain_value-domvalue_l } not available as constant| ).
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

ENDCLASS.
```
</details>

Moreover, classes enforce clean object orientation
through the additions `ABSTRACT` and `FINAL`.
Interfaces tempt people to "implement" them.
While this shortens their syntax by using the constants
without a leading `/dirty/message_severity=>`,
this kind of "inheritance out of convenience"
makes no sense in object orientation
and should be avoided.

```ABAP
" inferior pattern
INTERFACE /dirty/message_severity.
  CONSTANTS:
    warning TYPE symsgty VALUE 'W',
    error   TYPE symsgty VALUE 'E'.
ENDINTERFACE.
```
