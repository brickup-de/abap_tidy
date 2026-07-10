---
title: "Keep parameters behind the call"
weight: 130
date: 2026-07-11
params:
  license: "CC BY 3.0"
  license_url: "https://creativecommons.org/licenses/by/3.0/"
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#keep-parameters-behind-the-call"
---

```ABAP
DATA(sum) = add_two_numbers( value_1 = 5
                             value_2 = 6 ).
```

When this makes the lines very long, you can break the parameters into the next line:

```ABAP
DATA(sum) = add_two_numbers(
                value_1 = round_up( input DIV 7 ) * 42 + round_down( 19 * step_size )
                value_2 = VALUE #( ( `Calculation failed with a very weird result` ) ) ).
```
