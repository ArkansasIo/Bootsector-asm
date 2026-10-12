; CMOS/RTC register reader demonstration, 16-bit real mode.
; CMOS index port 70h, data port 71h. RTC values can be BCD or binary.
BITS 16
ORG 0x9000
cmos_demo:
    mov ax, 3
    int 0x10
    mov si, cmos_title
    call print_string
    mov al, 0x00
    call cmos_read
    mov [rtc_seconds], al
    mov al, 0x02
    call cmos_read
    mov [rtc_minutes], al
    mov al, 0x04
    call cmos_read
    mov [rtc_hours], al
    mov si, label_time
    call print_string
    mov al, [rtc_hours]
    call print_hex
    mov al, ':'
    call put_char
    mov al, [rtc_minutes]
    call print_hex
    mov al, ':'
    call put_char
    mov al, [rtc_seconds]
    call print_hex
    mov si, newline
    call print_string
    mov si, note
    call print_string
    ret
cmos_read:
    push dx
    push bx
    mov bl, al
    mov dx, 0x70
    mov al, bl
    or al, 0x80
    out dx, al
    mov dx, 0x71
    in al, dx
    push ax
    mov dx, 0x70
    xor al, al
    out dx, al
    pop ax
    pop bx
    pop dx
    ret
put_char:
    mov ah, 0x0E
    xor bh, bh
    int 0x10
    ret
print_string:
    lodsb
    test al, al
    jz .done
    call put_char
    jmp print_string
.done:
    ret
print_hex:
    push ax
    mov ah, al
    shr al, 4
    call print_nibble
    mov al, ah
    and al, 0x0F
    call print_nibble
    pop ax
    ret
print_nibble:
    and al, 0x0F
    cmp al, 9
    jbe .digit
    add al, 'A' - 10
    jmp put_char
.digit:
    add al, '0'
    jmp put_char
rtc_seconds db 0
rtc_minutes db 0
rtc_hours db 0
cmos_title db "CMOS / RTC REGISTER DEMO",13,10,0
label_time db "Raw RTC time (hex/BCD may vary): ",0
newline db 13,10,0
note db "Prototype: robust RTC synchronization and mode decoding are future work.",13,10,0
