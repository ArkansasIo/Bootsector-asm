; FloppyBootSuite Stage 1 boot sector
; NASM, 16-bit x86 BIOS, raw 512-byte sector.
; Loads eight sectors beginning at floppy CHS sector 2 to 0000:8000.
BITS 16
ORG 0x7C00

STAGE2_OFF     equ 0x8000
STAGE2_SECTORS equ 8

start:
    jmp 0x0000:boot_main
    nop

boot_main:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    sti
    cld
    mov [boot_drive], dl

    mov ax, 0x0003
    int 0x10
    mov si, msg_loading
    call print_string

    ; CHS cylinder 0, head 0, sector 2 = LBA 1 on a 1.44 MB floppy.
    mov ax, 0
    mov es, ax
    mov bx, STAGE2_OFF
    mov ah, 0x02
    mov al, STAGE2_SECTORS
    mov ch, 0
    mov cl, 2
    mov dh, 0
    mov dl, [boot_drive]
    int 0x13
    jc disk_error

    mov dl, [boot_drive]
    jmp 0x0000:STAGE2_OFF

disk_error:
    mov si, msg_error
    call print_string
    xor ah, ah
    int 0x16
    int 0x19
.halt:
    cli
    hlt
    jmp .halt

print_string:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0E
    mov bh, 0
    mov bl, 0x07
    int 0x10
    jmp print_string
.done:
    ret

boot_drive db 0
msg_loading db 13,10,"FloppyBootSuite: loading system...",13,10,0
msg_error   db 13,10,"Disk read failed. Press a key to reboot.",13,10,0

times 510-($-$$) db 0
dw 0xAA55
