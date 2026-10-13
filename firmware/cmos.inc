; CMOS_READ_BYTE: AL=register index, returns AL=value.
; Preserves BX/DX and restores the previous CMOS index/NMI-mask byte.
%ifndef FLOPPY_CMOS_INC
%define FLOPPY_CMOS_INC 1
cmos_read_byte:
    push bx
    push dx
    mov bl, al
    mov dx, 0x70
    in al, dx
    mov bh, al
    mov al, bl
    and al, 0x7F
    mov cl, bh
    and cl, 0x80
    or al, cl
    out dx, al
    mov dx, 0x71
    in al, dx
    mov bl, al
    mov dx, 0x70
    mov al, bh
    out dx, al
    mov al, bl
    pop dx
    pop bx
    ret
%endif
