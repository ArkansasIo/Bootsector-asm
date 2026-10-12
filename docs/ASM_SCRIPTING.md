# Assembly Scripting and Build Automation

“Scripting assembly” includes two related practices.

1. Assembler-time scripting: NASM macros, %define, %macro, %if, %include, and generated tables.
2. Host-side scripting: Python or shell scripts invoke NASM, build images, lint data, and run tests.

## NASM macro example
~~~asm
%macro BIOS_PRINT 1
    mov si, %1
    call bios_print_string
%endmacro

; Example use after including the shared routine:
; BIOS_PRINT message_label
~~~

Macros expand at assembly time; they are not runtime functions. Use CALL for a shared routine rather than duplicating a large macro body.

## Host build script
scripts/build.py stores targets in a declarative list and invokes NASM with subprocess using an argument array. This avoids shell-string interpolation and checks boot-sector size and signature.

~~~sh
python3 scripts/build.py
python3 scripts/menu_lint.py
~~~

## Data-driven menus
examples/scripted_menu.json defines a menu schema. scripts/menu_lint.py checks required fields, unique menu IDs, single-character keys, and duplicate key bindings. It currently validates the schema; it does not yet compile JSON into NASM tables or replace the hard-coded Stage 2 menu.

## Planned generator
A future generator can convert validated JSON into NASM strings or indexed menu records. It should escape quotes, reject unsupported control characters, enforce the 4096-byte Stage 2 limit, and produce deterministic output.
