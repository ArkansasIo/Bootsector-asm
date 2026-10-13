; BIOS keyboard helpers.
%ifndef FLOPPY_LIB_KEYBOARD_INC
%define FLOPPY_LIB_KEYBOARD_INC 1
keyboard_read_key:
    xor ah, ah
    int 0x16
    ret
keyboard_check_key:
    mov ah, 0x01
    int 0x16
    ret
%endif
