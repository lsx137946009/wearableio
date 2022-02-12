# WearableIO
Python tools for parsering wearable frame byte stream .

## Introduction
WearableIO is a framework to add support for parsering wearable frame byte stream. 

The wearable frame is expressed as a set of byte stream. For example

`<0x00 0xA1 0x14 0x00 ...>`
`<0x00 0xA1 0x14 0x01 ...>`

The wearable frame protocol design these frames consisted of different types of field, and each field combined several bytes. For example

Field name | Offset | Size | Value
---- | ----- | ------ | ---- 
Head Field | 0 | 2 | 0x00A1 
Length Field | 2 | 1 | 0x00 ~ 0x14
Type Field | 3 | 1 | 0x00 ~ 0xff
... | ... | ... | ...

With the pre-definded data protocol, the wearable frame would transfer to 

`<0x00 0xA1 0x14 0x00 ...>` -> `<Device Init1 Frame>`
`<0x00 0xA1 0x14 0x01 ...>` -> `<Device Init2 Frame>`
... ...

