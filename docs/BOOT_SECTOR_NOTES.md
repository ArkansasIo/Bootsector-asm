# Boot sector engineering notes

## BIOS entry conditions

Legacy BIOS loads the selected boot sector at physical address `0x7C00` and transfers control to it. The CPU enters 16-bit real mode, but robust boot code should not assume all segment registers, stack state, or direction flag values are already suitable. This project normalizes segment registers, sets a stack, clears DF, and saves the BIOS boot-drive number from `DL`.

## Stage 1 layout

A conventional 512-byte boot sector has the following layout:

| Offset | Length | Content |
|---:|---:|---|
| 0 | variable | Bootstrap instructions and data |
| 446 | 64 | MBR partition table, when the sector is an MBR |
| 510 | 2 | Boot signature bytes `55 AA` |

A floppy boot sector does not need an MBR partition table. The separate `boot/mbr.asm` target must preserve its partition table arrangement.

## Current Stage 1 load operation

`boot/boot.asm` reads eight sectors beginning at CHS sector 2 (the second sector of cylinder 0/head 0) into physical address `0x8000`, then jumps to `0000:8000`. This is a deliberate teaching simplification. It relies on floppy geometry and places a hard bound of 4096 bytes on Stage 2. A more capable loader should implement disk reset/retry logic and BIOS Enhanced Disk Drive (EDD) LBA reads where supported.

## Stage 2 and kernel boundary

Stage 2 initializes segment registers and stack, enters a BIOS text-mode menu, and presents static boot/disk/module/system/help/settings reference pages. The standalone `os/kernel.asm` is built as a separate binary and is not loaded by Stage 2 yet. A future loader must define a disk layout, read errors/retries, load address, memory-map ownership, and an explicit handoff ABI before integrating the kernel.

## Verification checklist

1. Stage 1 output is exactly 512 bytes.
2. Bytes 510–511 are `55 AA`.
3. Stage 2 is nonempty and fits within eight sectors (4096 bytes).
4. The disk image is 1,474,560 bytes.
5. Sector zero equals the assembled boot sector.
6. Stage 2 begins at LBA 1 (byte offset 512).
7. The stage 2 contents in the image equal the assembled Stage 2 binary.
8. The remaining bytes in the fixed eight-sector Stage 2 load window are zero-padded.

Run `make verify` after building with NASM and Make.

## Safe testing

Use a disposable QEMU image. Do not write a prototype bootloader directly to a physical disk. This project intentionally does not enable physical disk writes or CMOS configuration writes.
