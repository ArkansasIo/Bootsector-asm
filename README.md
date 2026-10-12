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


## Expanded design, pseudo-OOP assembly, and scripting

### New source examples
- `asm/oop_macros.inc` — conventions for structure-based objects.
- `examples/oop_counter.asm` — a Counter object with state and a method routine.
- `examples/scripted_menu.json` — data-driven menu schema.
- `scripts/build.py` — declarative NASM build orchestration.
- `scripts/menu_lint.py` — checks menu IDs, keys, labels, and targets.

### New documentation
- `docs/DESIGN.md` — architecture planes, boot contracts, and acceptance criteria.
- `docs/OOP_ASM.md` — object layouts, method conventions, dispatch, and ABI guidance.
- `docs/ASM_SCRIPTING.md` — NASM macros and host-side automation.
- `docs/ASM_ABI.md` — register, segment, stack, and calling conventions.
- `docs/MODULE_SPEC.md` — responsibilities and module contracts.
- `docs/TEST_MATRIX.md` — build and emulator test matrix.
- `CONTRIBUTING.md` — constraints for contributions.

### Additional commands
```sh
make scripted-build  # assemble all declared targets through Python
make lint            # validate scripted_menu.json
make oop-demo        # build the standalone pseudo-OOP example
```

NASM pseudo-OOP is a project convention: structures describe byte offsets, object instances occupy memory, and method routines accept documented pointers. It does not add native classes to assembly. The JSON menu currently gets validated, but is not yet compiled into the boot menu.
