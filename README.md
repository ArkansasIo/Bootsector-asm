# FloppyBootSuite / Bootsector-asm

An educational NASM x86 BIOS bootloader and operating-system learning project. Includes boot sector, stage-two text UI, MBR/VBR examples, BIOS service wrappers, CMOS/RTC demos, a real-mode kernel prototype, reusable assembly includes, configuration profiles, Python build/lint tools, and a small Tkinter assembly IDE.

## Requirements
- NASM
- GNU Make
- Python 3
- Tkinter for the graphical IDE (usually included with Python)
- QEMU `qemu-system-i386` for emulation

## Build and verify
```sh
make components
make image
make verify
make lint config-lint
```

Run the emulator with `make run`. Build an MBR test image with `make mbr-image`; this is an emulator-only test image.

Launch the IDE:
```sh
make ide
# or: python3 scripts/asm_ide.py
```
IDE shortcuts: Ctrl+O open, Ctrl+S save, F5 build, F6 lint, F9 run QEMU.

## UI application and API

Launch the browser-based control center and localhost JSON API:

```sh
python3 app.py
# or
make app
```

The dashboard opens at `http://127.0.0.1:8765`. Use `python3 app.py --no-browser` to suppress browser opening, or `python3 app.py --port 9000` to choose another local port. The API exposes health, toolchain status, project file inventory, settings, and allowlisted build/verify/lint/clean actions. API documentation: `docs/API_REFERENCE.md`.

Launch the desktop Tkinter source editor through the same entry point with `python3 app.py --desktop`. See `docs/APP_GUIDE.md` for usage and safety notes. The API binds to localhost only and does not expose arbitrary shell commands, CMOS writes, or physical disk writes.

## Components
- `boot/` — BIOS boot sector, MBR, and VBR
- `stage2/stage2.asm` — text menu including BIOS/CMOS settings reference
- `firmware/` — BIOS wrappers, BIOS build constants, CMOS/RTC helpers, JSON profiles
- `asm/lib/` — console, hex, keyboard, CHS disk, and memory helpers
- `os/kernel.asm` — separate real-mode kernel demo
- `scripts/asm_ide.py` — Tkinter source editor/build runner
- `scripts/build.py`, `scripts/config_lint.py` — build and settings validation
- `config/` and `language/` — boot settings and language/tooling docs
- `docs/` — architecture, ABI, boot flow, settings, libraries, and IDE guides

## Language and libraries
The source language is NASM x86 assembly. Shared code is included with `%include`; reusable routines document their register contracts. The project also uses Python for host-side tools and JSON for validated configuration/menu data. See `docs/LANGUAGE_REFERENCE.md` and `docs/ASSEMBLY_LIBRARIES.md`.

## Safety and limitations
This is an educational prototype, not a replacement BIOS or installable general-purpose OS. Configuration JSON does not change machine behavior unless a consumer explicitly reads it. CMOS writes and physical disk writes are disabled. Test generated images in QEMU, not on physical disks.
