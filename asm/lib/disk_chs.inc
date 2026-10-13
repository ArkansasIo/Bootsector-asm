; BIOS CHS read wrapper: AL=count, CH=cylinder, CL=sector,
; DH=head, DL=drive, ES:BX=destination. Carry flag reports BIOS result.
%ifndef FLOPPY_LIB_DISK_CHS_INC
%define FLOPPY_LIB_DISK_CHS_INC 1
disk_read_chs:
    mov ah, 0x02
    int 0x13
    ret
disk_reset:
    xor ah, ah
    int 0x13
    ret
%endif
