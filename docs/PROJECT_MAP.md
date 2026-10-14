# FloppyBootSuite — project map

This document maps the source tree to its runtime/build responsibilities. It describes the current prototype, not features that are only planned.

## Boot chain

```text
BIOS POST
  └─ boot/boot.asm (512-byte floppy boot sector)
       └─ BIOS INT 13h reads CHS sector 2 onward
            └─ stage2/stage2.asm at 0000:8000
                 └─ BIOS text UI / menu and diagnostics references
```

The MBR/VBR demos are separate targets. The real-mode kernel is assembled independently; Stage 2 does not yet load it.

## Directory map

| Path | Responsibility |
|---|---|
| `boot/` | Floppy boot sector, MBR demo, VBR/MBR demo |
| `stage2/` | Real-mode Stage 2 menu |
| `os/` | Standalone real-mode kernel prototype |
| `firmware/` | BIOS service includes and CMOS/RTC read-only demos |
| `asm/lib/` | Console, CHS disk, hex formatting, keyboard, memory helpers |
| `examples/` | Library and macro/object-style examples, scripted menu data |
| `config/` | Validated application and boot defaults |
| `language/` | Language/toolchain notes |
| `scripts/` | Build, lint, and Tkinter IDE |
| `tools/` | Host-side emulator-image construction |
| `api/` and `app/web/` | Localhost-only JSON API and browser control center |
| `tests/` | Boot-image verification and API unit tests |
| `docs/` | Architecture, ABI, APIs, user guides, and roadmap |
| `.github/workflows/` | Automated build/lint/test pipeline |

## Build tasks

- `make components`: assemble all declared NASM examples.
- `make image`: assemble Stage 1/Stage 2 and create a 1.44 MB floppy image.
- `make verify`: build the image and validate its size, signature, and layout.
- `make lint config-lint`: check scripted menu data and configuration JSON.
- `make mbr-image`: create the separate emulator-only MBR test image.
- `make ide`: launch the Tkinter source editor.
- `make app`: launch the local dashboard/API.

## Constraints

- Stage 1 must stay exactly 512 bytes and end in bytes `55 AA`.
- Stage 2 currently occupies up to eight sectors in the floppy image. Keep it within the 4096-byte sector-load bound unless the loader and image layout are changed together.
- The boot sector assumes a 1.44 MB floppy CHS geometry.
- The kernel is not yet integrated into Stage 2.
- Disk and CMOS writes remain out of scope; use QEMU for experiments.
