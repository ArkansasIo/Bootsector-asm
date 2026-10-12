# FloppyBootSuite / Bootsector-asm

A NASM x86 BIOS bootloader and operating-system learning project. Includes a 512-byte boot sector, stage-two text UI, an MBR example, a dedicated partition VBR, CMOS/RTC demo, tiny real-mode kernel, build scripts, and architecture docs.

## Requirements

- NASM
- GNU Make
- Python 3
- QEMU (`qemu-system-i386`) for emulation

## Build

```sh
make components
make image
make verify
make run
```

Build an MBR test image:

```sh
make mbr-image
qemu-system-i386 -drive file=build/mbr-test.img,format=raw -boot c
```

## Components

- `boot/boot.asm` — 512-byte BIOS boot sector
- `stage2/stage2.asm` — menu UI and submenu shell
- `boot/mbr.asm` — active-partition MBR bootstrap
- `boot/vbr_mbr.asm` — test partition volume boot record
- `firmware/bios_services.inc` — reusable BIOS service wrappers
- `firmware/cmos.asm` — CMOS/RTC register-read demonstration
- `os/kernel.asm` — separate real-mode kernel demo
- `docs/` — architecture, data model, UI, memory map, disk geometry, testing, and roadmap

## Important limitations

This is an educational prototype, not a complete installable OS or a replacement BIOS. The MBR image is an unformatted emulator test image. Do not test unfinished disk-writing code on physical media. NASM and QEMU builds should be run and verified locally before relying on the images.
