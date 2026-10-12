; FloppyBootSuite educational MBR.
; Locates the first active partition, reads its first sector to 0000:7E00,
; then transfers control. Partition table at 446..509, signature at 510..511.
BITS 16
ORG 0x7C00
start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00
    sti
    cld
    mov [boot_drive], dl
    mov si, partition_table
    mov cx, 4
.find_active:
    cmp byte [si], 0x80
    je .found
    add si, 16
    loop .find_active
    mov si, msg_no_partition
    call print_string
    jmp halt
.found:
    mov dh, [si + 1]
    mov cx, [si + 2]
    mov bx, 0x7E00
    mov ax, 0x0201
    mov dl, [boot_drive]
    int 0x13
    jc .read_error
    mov dl, [boot_drive]
    jmp 0x0000:0x7E00
.read_error:
    mov si, msg_read_error
    call print_string
    jmp halt
print_string:
    lodsb
    test al, al
    jz .done
    mov ah, 0x0E
    mov bh, 0
    mov bl, 7
    int 0x10
    jmp print_string
.done:
    ret
halt:
    xor ah, ah
    int 0x16
    int 0x19
.dead:
    cli
    hlt
    jmp .dead
boot_drive db 0
msg_no_partition db 13,10,"MBR: no active partition found.",13,10,0
msg_read_error db 13,10,"MBR: failed to read partition boot sector.",13,10,0
times 446-($-$$) db 0
partition_table:
    times 64 db 0
dw 0xAA55
