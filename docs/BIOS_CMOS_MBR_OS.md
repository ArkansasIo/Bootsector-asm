# BIOS, CMOS/RTC, MBR, and OS layers

## BIOS firmware boundary
BIOS is motherboard firmware, not a normal application. This project invokes existing firmware services:
- INT 10h: video
- INT 13h: disk
- INT 16h: keyboard
- INT 19h: bootstrap/reboot handoff

`firmware/bios_services.inc` provides small wrappers; it is not a BIOS replacement.

## CMOS and RTC
`firmware/cmos.asm` demonstrates reading RTC second, minute, and hour registers via CMOS ports 70h/71h. Production code must synchronize around the update-in-progress bit, respect NMI masking policy, and decode BCD/binary plus 12/24-hour modes.

## MBR
`boot/mbr.asm` is exactly 512 bytes with:
- bytes 0-445: bootstrap code/data
- bytes 446-509: four 16-byte partition entries
- bytes 510-511: signature 55 AA

The demo uses active-partition CHS, does not fully validate partition bounds, and is for emulator learning only. Production boot code should check INT 13h extensions and prefer LBA reads where supported.

## OS kernel
`os/kernel.asm` is a separate real-mode shell. It is not yet automatically loaded from Stage 2.

## Boot paths
Floppy prototype: BIOS POST -> boot sector -> stage 2 menu
MBR prototype: BIOS POST -> MBR -> partition VBR -> stage 2 menu
Future OS path: BIOS POST -> MBR -> VBR -> stage 2 loader -> kernel
