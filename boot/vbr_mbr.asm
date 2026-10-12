; Partition VBR loaded by MBR at 0000:7E00.
; Stage 2 is stored at LBA 2 / CHS sector 3 in the test image.
BITS 16
ORG 0x7E00
STAGE2_OFF equ 0x8000
STAGE2_SECTORS equ 8
start:
    jmp 0x0000:vbr_main
    nop
vbr_main:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7A00
    sti
    cld
    mov [boot_drive], dl
    mov si, loading
    call print_string
    mov ax, 0
    mov es, ax
    mov bx, STAGE2_OFF
    mov ah, 0x02
    mov al, STAGE2_SECTORS
    mov ch, 0
    mov cl, 3
    mov dh, 0
    mov dl, [boot_drive]
    int 0x13
    jc disk_error
    mov dl, [boot_drive]
    jmp 0x0000:STAGE2_OFF
disk_error:
    mov si, error
    call print_string
    xor ah, ah
    int 0x16
    int 0x19
print_string:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0E
    xor bh, bh
    mov bl, 7
    int 0x10
    jmp print_string
.done:
    ret
boot_drive db 0
loading db 13,10,"FloppyBootSuite MBR partition VBR...",13,10,0
error db 13,10,"VBR: disk read failed.",13,10,0
times 510-($-$$) db 0
dw 0xAA55
