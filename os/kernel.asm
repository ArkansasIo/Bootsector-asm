; Tiny 16-bit real-mode OS shell prototype.
; Separate binary entry at physical 9000h; not loaded by the default stage 2.
BITS 16
ORG 0x9000
kernel_entry:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7A00
    sti
    cld
    mov ax, 3
    int 0x10
    mov si, os_banner
    call print_string
.main:
    mov si, os_menu
    call print_string
    xor ah, ah
    int 0x16
    cmp al, '1'
    je .about
    cmp al, '2'
    je .firmware
    cmp al, 'q'
    je .reboot
    cmp al, 'Q'
    je .reboot
    jmp .main
.about:
    mov si, about_text
    call print_string
    jmp .main
.firmware:
    mov si, firmware_text
    call print_string
    jmp .main
.reboot:
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
    xor bh, bh
    mov bl, 7
    int 0x10
    jmp print_string
.done:
    ret
os_banner db 13,10,"FloppyBootSuite OS Kernel Demo",13,10,"================================",13,10,0
os_menu db 13,10,"1. About this kernel",13,10,"2. BIOS/firmware boundary",13,10,"Q. Reboot",13,10,"Select: ",0
about_text db 13,10,"Tiny real-mode kernel shell; not a general-purpose OS.",13,10,0
firmware_text db 13,10,"BIOS video/keyboard/disk services use software interrupts.",13,10,0
