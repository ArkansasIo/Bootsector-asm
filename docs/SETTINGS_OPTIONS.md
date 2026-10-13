# Settings and options

## Configuration files
- `config/boot_options.json`: loader and emulator defaults.
- `firmware/bios_profile.json`: BIOS service profile and retry policy.
- `firmware/cmos_registers.json`: RTC register map.
- `examples/scripted_menu.json`: menu schema, including a settings reference submenu.

JSON settings describe host tooling and future generated code. Unless a consumer is explicitly wired to read a setting, changing JSON does not alter the assembled boot sector. Stage 2 option 6 is a read-only description of the defaults.

Physical disk writes remain disabled. Image creation targets files under `build/`. CMOS writes are not implemented. Exercise hardware-facing code in QEMU first.
