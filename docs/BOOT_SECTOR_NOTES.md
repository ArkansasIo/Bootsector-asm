# Boot sector engineering notes

## BIOS entry conditions

Legacy BIOS loads the selected boot sector at physical address `0x7C00` and transfers control to it. Robust boot code should normalize segment registers, establish a stack, clear the direction flag, and preserve the boot-drive number passed in `DL`. The current Stage 1 performs these setup steps.

## Stage 1 layout

| Offset | Length | Content |
|---:|---:|---|
| 0 | variable | Bootstrap instructions and data |
| 446 | 64 | MBR partition table, for MBR mode |
| 510 | 2 | Boot signature bytes `55 AA` |

The floppy boot sector does not need an MBR partition table. The separate `boot/mbr.asm` target must preserve the partition-table layout.

## Current Stage 1 load operation

`boot/boot.asm` reads eight sectors beginning at CHS sector 2 (the second sector of cylinder 0/head 0) into physical address `0x8000`, then jumps to `0000:8000`. This is a teaching simplification dependent on floppy geometry and imposes a 4096-byte limit on Stage 2. Future iterations can add disk reset/retry handling and BIOS Enhanced Disk Drive (EDD) LBA reads.

## Stage 2 and kernel boundary

Stage 2 initializes segments and the stack, enters BIOS text mode, and presents static menu/reference pages. `os/kernel.asm` is assembled separately and is not loaded by Stage 2 yet. Kernel integration requires a defined disk layout, load address, error handling, memory ownership, and handoff ABI.

## Verification checklist

1. Stage 1 is exactly 512 bytes.
2. Bytes 510–511 are `55 AA`.
3. Stage 2 is nonempty and fits in eight sectors (4096 bytes).
4. The image is 1,474,560 bytes.
5. Image LBA 0 matches the assembled Stage 1.
6. Stage 2 starts at LBA 1 (byte offset 512).
7. The Stage 2 bytes in the image match the assembled binary.
8. Remaining bytes in the fixed Stage 2 load window are zero-filled.

Run `make verify` after assembling with NASM and Make.

## Safe testing

Use a disposable QEMU image. Do not write a prototype bootloader directly to a physical disk. This project intentionally excludes physical disk writes and CMOS configuration writes.
