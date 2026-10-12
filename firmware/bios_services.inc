; BIOS service wrappers for 16-bit real mode.
; These use firmware already present on compatible machines.
bios_video_mode3:
    mov ax, 0x0003
    int 0x10
    ret
bios_print_string:
.next:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0E
    mov bh, 0
    mov bl, 7
    int 0x10
    jmp .next
.done:
    ret
bios_wait_key:
    xor ah, ah
    int 0x16
    ret
bios_reset_disk:
    xor ah, ah
    int 0x13
    ret
