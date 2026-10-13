; hex_print_byte prints AL as two uppercase hexadecimal characters.
%ifndef FLOPPY_LIB_HEX_INC
%define FLOPPY_LIB_HEX_INC 1
hex_print_byte:
    push bx
    push dx
    mov bl, al
    mov al, bl
    shr al, 4
    call hex_print_nibble
    mov al, bl
    and al, 0x0F
    call hex_print_nibble
    pop dx
    pop bx
    ret
hex_print_nibble:
    and al, 0x0F
    cmp al, 9
    jbe .digit
    add al, 'A' - 10
    jmp .emit
.digit:
    add al, '0'
.emit:
    mov ah, 0x0E
    xor bh, bh
    int 0x10
    ret
%endif
