# Assembly IDE and tooling

`scripts/asm_ide.py` is a lightweight host-side IDE with a source tree, editor, build action, configuration lint, and optional QEMU launch. It is not a CPU emulator or source-level debugger.

## Launch
```sh
python3 scripts/asm_ide.py
```
Requires Python 3 and Tkinter. NASM is required to build; QEMU is required to run.

## Keyboard
- Ctrl+O: open file
- Ctrl+S: save
- F5: build NASM targets
- F6: lint menu/configuration
- F9: launch QEMU if installed

Reusable includes are in `asm/lib/`; BIOS and CMOS/RTC support is in `firmware/`. Build output stays under `build/`; the IDE must not write to physical disks.
