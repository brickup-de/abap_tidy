---
title: "Avoid obsolete language elements"
weight: 50
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#avoid-obsolete-language-elements"
---

When upgrading your ABAP version,
make sure to check for obsolete language elements
and refrain from using them.

For example, the `@`-escaped "host" variables
in the following statement make a little clearer
what's a program variable and what's a column in the database,

```ABAP
SELECT *
  FROM spfli
  WHERE carrid = @carrid AND
        connid = @connid
  INTO TABLE @itab.
```

as compared to the [obsolete unescaped form](https://help.sap.com/doc/abapdocu_750_index_htm/7.50/en-US/abenopen_sql_hostvar_obsolete.htm)

```ABAP
SELECT *
  FROM spfli
  WHERE carrid = carrid AND
        connid = connid
  INTO TABLE itab.
```

Newer alternatives tend to improve readability of the code,
and reduce design conflicts with modern programming paradigms,
such that switching to them can automatically clean your code.

While continuing to work, obsolete elements may stop benefitting
from optimizations in terms of processing speed and memory consumption.

With modern language elements, you can onboard young ABAPers easier,
who may no longer be familiar with the outdated constructs
because they are no longer taught in SAP's trainings.

The SAP NetWeaver documentation contains a stable section
that lists obsolete language elements, for example
[NW 7.50](https://help.sap.com/doc/abapdocu_750_index_htm/7.50/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.51](https://help.sap.com/doc/abapdocu_751_index_htm/7.51/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.52](https://help.sap.com/doc/abapdocu_752_index_htm/7.52/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.53](https://help.sap.com/doc/abapdocu_753_index_htm/7.53/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.54](https://help.sap.com/doc/abapdocu_754_index_htm/7.54/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.55](https://help.sap.com/doc/abapdocu_755_index_htm/7.55/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.56](https://help.sap.com/doc/abapdocu_756_index_htm/7.56/en-US/index.htm?file=abenabap_obsolete.htm),
[NW 7.57](https://help.sap.com/doc/abapdocu_757_index_htm/7.57/en-US/index.htm?file=abenabap_obsolete.htm).
