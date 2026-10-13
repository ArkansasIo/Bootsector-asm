# IDE quick reference

Launch with `python3 scripts/asm_ide.py`. Use the file tree to open source/config files. Ctrl+S saves; F5 assembles declared targets; F6 validates menu and JSON config; F9 launches QEMU if installed.

The IDE invokes subprocesses with argument arrays and confines editor saves to repository paths. It is a lightweight editor/build runner, not a full debugger.
