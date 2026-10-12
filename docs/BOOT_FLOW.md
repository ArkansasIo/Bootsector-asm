# Boot Flow

## Floppy image
BIOS POST -> `boot/boot.asm` sector 0 -> stage 2 at 0000:8000 -> text menu.

## MBR test image
BIOS POST -> `boot/mbr.asm` -> active partition entry -> `boot/vbr_mbr.asm` -> stage 2 -> text menu.

## Kernel demo
`os/kernel.asm` is assembled separately at ORG 9000h. The current Stage 2 menu does not load it yet. Integrating it requires a loader entry, reserved memory layout, and a kernel handoff contract.

## Security and reliability notes
- The MBR is educational and currently uses CHS only.
- Partition range validation and EDD/LBA support are not implemented.
- The test partition is not a formatted FAT volume.
- Run only in QEMU/Bochs while developing; never use test code against disks with important data.
