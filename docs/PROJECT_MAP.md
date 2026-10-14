# FloppyBootSuite — project map

A directory map and overview of the existing bootloader prototype.

## Boot chain

`boot/boot.asm` is the 512-byte floppy boot sector. It reads eight sectors beginning at CHS sector 2 into physical address `0x8000`, then jumps to `0000:8000` for `stage2/stage2.asm`. The MBR/VBR demos are separate targets. `os/kernel.asm` is assembled independently and is not yet loaded by Stage 2.

## Directory map

| Path | Responsibility |
|---|---|
| `boot/` | Floppy boot sector, MBR and VBR examples |
| `stage2/` | Real-mode Stage 2 menu |
| `os/` | Standalone real-mode kernel prototype |
| `firmware/` | BIOS includes and read-only CMOS/RTC demos |
| `asm/lib/` | Console, CHS disk, hex, keyboard and memory helpers |
| `examples/` | Library and macro/object-style examples, scripted menu data |
| `config/` | Application and boot defaults |
| `scripts/` | Build, lint and Tkinter IDE |
| `tools/` | Host-side test-image builder |
| `api/`, `app/web/` | Localhost JSON API and browser control center |
| `tests/` | Image verifier and API tests |
| `docs/` | Architecture, ABI, API and user guides |
| `.github/workflows/` | Automated CI |

## Build tasks

- `make components`: assemble the declared NASM examples.
- `make image`: create a 1.44 MB floppy image.
- `make verify`: validate image size, signature and layout.
- `make lint config-lint`: validate menu/configuration data.
- `make mbr-image`: create the emulator-only MBR test image.
- `make ide`: launch the Tkinter editor.
- `make app`: launch the local dashboard/API.

## Constraints

Stage 1 must remain exactly 512 bytes and end with `55 AA`. Stage 2 must fit in the fixed eight-sector (4096-byte) load window. The boot sector assumes 1.44 MB floppy CHS geometry. CMOS writes and physical disk writes are intentionally out of scope; test with QEMU.
