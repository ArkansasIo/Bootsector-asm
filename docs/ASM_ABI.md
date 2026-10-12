# 16-bit Real-Mode Assembly ABI

## General conventions
- Target: 16-bit real mode with BIOS interrupts.
- Registers are caller-clobbered unless a routine documents preservation.
- Return values use AX/AL unless specified otherwise.
- String pointer: DS:SI, zero-terminated.
- OOP demo object pointer: DS:BX.
- Keep stack balance across every call and interrupt wrapper.

## BIOS boundary
BIOS may modify registers. Save values needed after INT 10h, INT 13h, or INT 16h. Capture BIOS boot drive from DL before disk reads and restore it before stage handoff.

## Segment model
Physical address = segment * 16 + offset. A near pointer is a 16-bit offset interpreted through the current segment. Use far pointers or explicit segment:offset pairs when crossing segment boundaries.

## Stack
Stack grows downward. Keep stack storage away from code, loaded stages, and data. The samples initialize SP near 0x7A00; review this layout before adding larger buffers.

## Routine documentation template
~~~text
Routine: Module_method
Input: DS:BX -> object
Output: AX = result
Clobbers: AX, flags
Preserves: BX, CX, DX, SI, DI, BP, DS, ES
Errors: carry flag set on failure
~~~
