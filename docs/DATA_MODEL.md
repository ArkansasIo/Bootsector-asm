# Data Model: Classes, Types, Subtypes, Arrays

NASM assembly does not provide a runtime class system. This document defines the conceptual schema and ownership boundaries.

## Enumerations
- `BootStatus`: Cold, Initializing, Stage2Loaded, Ready, DiskReadError, FatalError
- `MenuId`: Main, BootOptions, DiskTools, Modules, Diagnostics, Help
- `DiskOperation`: Inspect, ReadImage, CloneImage (planned), VerifyImage

## Structures
### BootContext
| Field | Type | Meaning |
|---|---|---|
| boot_drive | u8 | BIOS drive number captured from DL |
| status | BootStatus | boot state |
| stage2_segment | u16 | stage two segment |
| stage2_offset | u16 | stage two offset |
| last_bios_error | u8 | last BIOS error |

### FloppyGeometry
| Field | Type | Standard value |
|---|---|---:|
| bytes_per_sector | u16 | 512 |
| sectors_per_track | u8 | 18 |
| heads | u8 | 2 |
| cylinders | u16 | 80 |
| total_sectors | u32 | 2880 |

### MenuEntry
| Field | Type | Meaning |
|---|---|---|
| key | u8 | activation key |
| label | string reference | text label |
| target_menu | MenuId | destination |
| flags | bit field | enabled/destructive/hidden |

## Type hierarchy
Primitive -> unsigned integers (u8/u16/u32), byte arrays, fixed strings, 16-bit pointers.
Domain types -> BootStatus, MenuId, DiskOperation, BIOSStatus.
Structures -> BootContext, FloppyGeometry, MenuEntry, MenuTable, ImageReport.

## Arrays and subarrays
- `menu_entries[]`: menu entry array
- `disk_menu_entries[]`: disk submenu entries
- `sector_buffer[512]`: one sector
- `stage2_buffer[4096]`: stage-two load window
- `sector_checksums[]`: optional per-sector verification output

On real-mode targets arrays are byte ranges with manual bounds. Validate offset plus length before buffer access.
