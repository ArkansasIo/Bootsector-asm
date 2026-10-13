# BIOS, CMOS/RTC, MBR, and OS layers

## BIOS firmware boundary
BIOS is motherboard firmware, not a normal application. This project calls existing firmware services:
- INT 10h: video
- INT 13h: disk
- INT 16h: keyboard
- INT 19h: bootstrap/reboot handoff

`firmware/bios_services.inc` provides reusable wrappers; it is not a BIOS replacement. `firmware/bios_settings.inc` defines build-time constants. The JSON BIOS profile documents defaults for host tools; it is not a live setup utility.

## CMOS and RTC
`firmware/cmos.asm` and `firmware/rtc_snapshot_demo.asm` are educational readers for RTC registers through ports 70h/71h. Production code must handle update-in-progress, BCD/binary mode, 12/24-hour mode, and platform differences. CMOS writes are intentionally not implemented.

## MBR
`boot/mbr.asm` is exactly 512 bytes with bootstrap/data, four partition entries, and signature 55 AA. The demo uses active-partition CHS and is for emulator learning only. Prefer validated LBA reads for a more capable loader.

## OS kernel
`os/kernel.asm` is a separate real-mode shell and is not yet automatically loaded by Stage 2.

## Boot paths
Floppy prototype: BIOS POST -> boot sector -> stage 2 menu.
MBR prototype: BIOS POST -> MBR -> partition VBR -> stage 2 menu.
Future OS path: BIOS POST -> MBR -> VBR -> stage 2 loader -> kernel.
