# FloppyBootSuite / Bootsector-asm

An educational NASM x86 BIOS bootloader and operating-system learning project. Includes a 512-byte boot sector, Stage 2 text UI, MBR/VBR examples, BIOS service wrappers, read-only CMOS/RTC demos, a standalone real-mode kernel prototype, reusable assembly includes, configuration profiles, Python build/lint tools, a Tkinter assembly IDE, and a localhost browser control center.

## Requirements

- NASM
- GNU Make
- Python 3
- Tkinter for the desktop IDE (usually included with Python)
- QEMU `qemu-system-i386` for emulation

## Build, lint, and verify

```sh
make components
make image
make verify
make lint config-lint
python3 -m unittest discover -s tests
```

Run the floppy image with `make run`. Build an MBR test image with `make mbr-image`; it is for emulator testing only.

## Applications

Desktop source editor:

```sh
make ide
# or: python3 scripts/asm_ide.py
```

Shortcuts: Ctrl+O open, Ctrl+S save, F5 build, F6 lint, F9 run QEMU.

Local browser dashboard and JSON API:

```sh
python3 app.py
# or: make app
```

Open `http://127.0.0.1:8765`. Use `python3 app.py --no-browser` to suppress browser opening or `python3 app.py --port 9000` to choose another local port. The API exposes health, toolchain status, a file inventory, settings, and allowlisted build/verify/lint/clean actions. API documentation: [docs/API_REFERENCE.md](docs/API_REFERENCE.md).

## Project map

- `boot/` — BIOS boot sector, MBR, and VBR examples
- `stage2/stage2.asm` — BIOS text-mode menu
- `firmware/` — BIOS service wrappers and CMOS/RTC read-only demos
- `asm/lib/` — console, hex, keyboard, CHS disk, and memory helpers
- `os/kernel.asm` — separate real-mode kernel demo, not yet loaded by Stage 2
- `scripts/` — assembly IDE, build scripts, and linters
- `api/` and `app/web/` — localhost-only dashboard/API
- `tests/` — image verification and unit tests
- `docs/PROJECT_MAP.md` — project structure and runtime map
- `docs/BOOT_SECTOR_NOTES.md` — boot contract, image layout, and validation

The source language is NASM x86 assembly. Host-side tooling uses Python; project profiles and scripted menu data use JSON. See [docs/LANGUAGE_REFERENCE.md](docs/LANGUAGE_REFERENCE.md) and [docs/ASSEMBLY_LIBRARIES.md](docs/ASSEMBLY_LIBRARIES.md).

## Safety and limitations

This is an educational prototype, not a replacement BIOS or installable general-purpose OS. Stage 2 uses a fixed eight-sector CHS load and the standalone kernel is not yet integrated. JSON profiles describe application defaults; they do not change live firmware settings. CMOS writes and physical disk writes are disabled. Test generated images in QEMU, not on physical disks.

More detail: [Architecture](docs/ARCHITECTURE.md) · [Boot flow](docs/BOOT_FLOW.md) · [API reference](docs/API_REFERENCE.md) · [Roadmap](docs/ROADMAP.md).
