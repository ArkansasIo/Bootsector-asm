; Reads raw RTC registers via shared CMOS include; intended for emulator testing.
BITS 16
ORG 0x9000
%include "firmware/cmos.inc"
%include "asm/lib/console.inc"
%include "asm/lib/hex.inc"
start:
    mov si, title
    call console_puts
    mov al, 0x00
    call cmos_read_byte
    call hex_print_byte
    mov al, ':'
    call console_putc
    mov al, 0x02
    call cmos_read_byte
    call hex_print_byte
    mov al, ':'
    call console_putc
    mov al, 0x04
    call cmos_read_byte
    call hex_print_byte
    call console_newline
.halt:
    cli
    hlt
    jmp .halt
title db "Raw RTC registers (seconds:minutes:hours) = ",0
