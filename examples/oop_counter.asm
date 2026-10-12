; Example: object-like data + method routine in NASM.
; Standalone real-mode demo binary; not part of the boot image.
BITS 16
ORG 0x9000
struc Counter
    .value: resw 1
    .step: resw 1
endstruc
start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7A00
    sti
    mov ax, 3
    int 0x10
    mov word [counter_a + Counter.value], 0
    mov word [counter_a + Counter.step], 1
    mov si, banner
    call print_string
    mov cx, 5
.loop:
    mov bx, counter_a
    call Counter_increment
    mov ax, [counter_a + Counter.value]
    call print_u16
    mov al, ' '
    call put_char
    loop .loop
    mov si, newline
    call print_string
.wait:
    xor ah, ah
    int 0x16
    int 0x19

; Method convention: DS:BX points to a Counter instance.
Counter_increment:
    push ax
    mov ax, [bx + Counter.step]
    add [bx + Counter.value], ax
    pop ax
    ret

print_u16:
    push ax
    push bx
    push cx
    push dx
    xor cx, cx
    mov bx, 10
    test ax, ax
    jnz .convert
    mov al, '0'
    call put_char
    jmp .done
.convert:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz .convert
.emit:
    pop dx
    mov al, dl
    add al, '0'
    call put_char
    loop .emit
.done:
    pop dx
    pop cx
    pop bx
    pop ax
    ret

print_string:
    lodsb
    test al, al
    jz .done
    call put_char
    jmp print_string
.done:
    ret
put_char:
    mov ah, 0x0E
    xor bh, bh
    mov bl, 7
    int 0x10
    ret

counter_a:
    istruc Counter
        at Counter.value, dw 0
        at Counter.step, dw 1
    iend
banner db "Pseudo-OOP ASM Counter: ",0
newline db 13,10,"Press a key to reboot.",13,10,0
