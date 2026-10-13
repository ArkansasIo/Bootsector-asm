; Demonstrates reusable console and hexadecimal includes.
BITS 16
ORG 0x9000
%include "asm/lib/console.inc"
%include "asm/lib/hex.inc"
start:
    mov si, demo_title
    call console_puts
    mov al, 0x5A
    call hex_print_byte
    call console_newline
.halt:
    cli
    hlt
    jmp .halt
demo_title db "Assembly library demo: byte=0x",0
