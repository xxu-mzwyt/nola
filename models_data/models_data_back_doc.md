```json
{
    "1": { 
        "fuel_type": "gasoline", 
        "mpg_city": "14.1316", 
        "mpg_highway": "11.9871", 
        "co2": "378"
    },
    ...
}
```

`key `:unique identification number

`"fuel_type"`: 

| gasoline, diesel | mile per gallon                             |
| ---------------- | ------------------------------------------- |
| electric, cng    | gasoline equivalent miles per gallon (MPGe) |
| hybrid           | Average MPGe (if use two powers evenly)     |
| pi-hybrid        | EPA composite gasoline-electricity MPGe     |

`"mpg_city"`: MPG or MPGe

`"mpg_highway"`: MPG or MPGe

`"co2"`: tailpipe CO2 in grams/mile