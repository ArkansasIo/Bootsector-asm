# NASM x86 Real-Mode Language Reference

## Minimal file
```asm
BITS 16
ORG 0x8000
start:
    mov ax, 0x0003
    int 0x10
.halt:
    hlt
    jmp .halt
```

## Syntax and directives
- Labels define addresses; dot-prefixed local labels belong to the preceding non-local label.
- `DB`, `DW`, `DD`, `RESB`, `EQU`, `%define`, `%include`, and `%macro` are common declarations.
- `BITS 16` selects instruction encoding; `ORG` sets the assumed origin for flat binaries.
- `CALL`/`RET` are near calls unless a module says otherwise.
- BIOS interrupts are firmware contracts, not project-defined OS syscalls.

## Calling convention
Document routine inputs, outputs, flags, preserved registers, and clobbers. Use DS:SI for NUL-terminated strings and ES:DI/CX for destination/count memory helpers. Segment registers and stack state are shared machine state.

## Safety
Validate disk geometry and request sizes before INT 13h. Do not write physical disks from development tools. Bound hardware polling loops. Inspect RTC status register B before assuming BCD/binary encoding. Boot sectors must be exactly 512 bytes with 55 AA at offsets 510-511.
