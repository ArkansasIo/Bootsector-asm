# FloppyBootSuite — System Design Specification

## Goals
- Demonstrate legacy x86 BIOS boot flow in 16-bit real mode.
- Keep first-stage sectors deterministic and size-constrained.
- Separate bootstrap, loader UI, firmware demos, kernel prototype, and host tooling.
- Document object-like assembly conventions and data-driven menu/build scripting.
- Keep destructive disk operations out of the boot UI until safety checks exist.

## Architecture planes

| Plane | Responsibilities | Source |
|---|---|---|
| Firmware | POST and BIOS interrupt services | Existing machine/VM BIOS |
| Bootstrap | Load next stage and transfer control | boot/boot.asm, boot/mbr.asm |
| Volume loader | Load stage 2 from test partition | boot/vbr_mbr.asm |
| Loader UI | Menus and status pages | stage2/stage2.asm |
| Kernel prototype | Separate real-mode entry point | os/kernel.asm |
| Hardware demo | CMOS/RTC port access | firmware/cmos.asm |
| Host automation | Build, lint, image generation, verification | scripts/ and tools/ |
| Documentation | Contracts, layouts, testing, roadmap | docs/ |

## Boot contracts

### Floppy image
BIOS loads sector 0 at physical 0x7C00. Stage 1 reads eight sectors beginning at CHS (0,0,2) into physical 0x8000, then jumps to 0000:8000.

### MBR test image
BIOS loads the MBR at 0x7C00. The MBR searches four partition entries for status 0x80, loads the partition boot sector at 0x7E00, then jumps there. The test VBR loads stage 2 from CHS (0,0,3) into 0x8000.

These are teaching examples. The MBR is CHS-only, validates only a small subset of partition data, and is not production-safe.

## Memory layout
- Stage 1: 0x7C00–0x7DFF
- MBR-loaded VBR: 0x7E00–0x7FFF
- Stage 2: 0x8000–0x8FFF, maximum 4096 bytes
- CMOS demo and kernel examples are separate binaries assembled at ORG 0x9000
- Stack starts near 0x7A00 and grows downward

## Non-goals
- Replacing motherboard BIOS firmware.
- Secure boot, UEFI, GPT, protected mode, paging, or SMP.
- A fully installable FAT-formatted OS.
- Physical-disk cloning or writes.
- Native OOP language semantics in NASM.

## Acceptance criteria
- Stage 1, MBR and VBR are exactly 512 bytes with 55 AA signature.
- Stage 2 remains within the initial 4096-byte read window.
- Menu JSON passes schema checks.
- Host image builder and tests pass.
- Both images are tested in QEMU before declaring the build verified.
