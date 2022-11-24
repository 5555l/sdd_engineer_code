# SDD engineer code generator

Generate SDD engineer passwords for functions such as CCF editing.

It only needs to know the `seed` and the `type` (Jaguar/Landrover) in order to generate the `password` for CCF editing. However it's advised to always provide `--vin` with `--seed` to ensure the seed matches the target vehicle to prevent incorrect passwords being generated.

If you don't provide a `VIN` it will output the last 6 digits of the `VIN` that it derives from the `seed` so you can double check it against the vehicle `VIN` to make sure it matches.

There maybe a security lockout by SDD or the ECU if you send it too many incorrect passwords - this is a presumption and has not been tested, don't blame me if you lockup your modules because you didn't check the `seed` matched the `VIN`.

## Arguments

| Argument | Description |
|:------|:------------|
|`-v / --vin <VIN>`|VIN of the target vehicle|
|`-s / --seed <seed>`|SDD seed of the target vehicle|
|`--g / --gen`|Generate a seed for the provided `VIN` - will override `--seed`. This option probably isn't very useful in real life, it's mostly used for testing this code|
|`-t / --type <JAG ¦ LR>`|Manually set vehicle type to Jaguar or Landrover instead of trying work it out from the `VIN`|
|`-o / --option <option>`|[SDD access option](#sdd-access-option), it will default to `CCF_EDITOR` if this isn't provided|

It's mandatory to provide at least one of these combinations:

 `--seed` and `--type`

 `--vin` and `--gen`

## SDD access option

| Brand | Option |
|:------|:------------|
|Jaguar| |
| |`X351_ODO_APP`|
| |`SOFTWARE_DOWNLOAD`|
| |`X250_ODO_APP`|
| |`CCF_EDITOR`|
| |`X150_ODO_APP`|
| |`VIN_BLOCK_EDITOR`|
| |`VIN_BYPASS`|
| |`X351_RECOVER_KEYS`|
|Landrover| |
| |`TAIWAN_VEHICLE_UPDATE`|
| |`L316_ODO_APP`|
| |`SOFTWARE_DOWNLOAD`|
| |`L322_ERASE_KEYS`|
| |`L322_RECOVER_KEYS`|
| |`L322_ODO_APP`|
| |`OPTION_8`|
| |`CCF_EDITOR`|

## Tested configurations

| Brand | Range | Model Year |
|:------|:-----|:------------|
|Jaguar|X250|2008|
|Jaguar|X250|2010|

Feedback about working with other VIN's would be useful
