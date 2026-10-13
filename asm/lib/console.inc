; BIOS teletype output helpers. DS:SI -> NUL-terminated string.
%ifndef FLOPPY_LIB_CONSOLE_INC
%define FLOPPY_LIB_CONSOLE_INC 1
console_putc:
    mov ah, 0x0E
    xor bh, bh
    mov bl, 7
    int 0x10
    ret
console_puts:
    push si
.next:
    lodsb
    test al, al
    jz .done
    call console_putc
    jmp .next
.done:
    pop si
    ret
console_newline:
    mov al, 13
    call console_putc
    mov al, 10
    call console_putc
    ret
%endif
