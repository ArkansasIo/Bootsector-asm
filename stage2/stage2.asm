; FloppyBootSuite Stage 2 text UI
BITS 16
ORG 0x8000

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7A00
    sti
    cld
    mov ax, 0x0003
    int 0x10
    call draw_main

main_loop:
    xor ah, ah
    int 0x16
    cmp al, '1'
    je menu_boot
    cmp al, '2'
    je menu_disk
    cmp al, '3'
    je menu_modules
    cmp al, '4'
    je menu_system
    cmp al, '5'
    je menu_help
    cmp al, '6'
    je menu_settings
    cmp al, 'q'
    je reboot
    cmp al, 'Q'
    je reboot
    jmp main_loop

menu_boot:
    call clear_screen
    mov si, title_boot
    call print_string
    mov si, boot_options
    call print_string
    call wait_back
    call draw_main
    jmp main_loop
menu_disk:
    call clear_screen
    mov si, title_disk
    call print_string
    mov si, disk_options
    call print_string
    call wait_back
    call draw_main
    jmp main_loop
menu_modules:
    call clear_screen
    mov si, title_modules
    call print_string
    mov si, module_options
    call print_string
    call wait_back
    call draw_main
    jmp main_loop
menu_system:
    call clear_screen
    mov si, title_system
    call print_string
    mov si, system_options
    call print_string
    call wait_back
    call draw_main
    jmp main_loop
menu_help:
    call clear_screen
    mov si, title_help
    call print_string
    mov si, help_options
    call print_string
    call wait_back
    call draw_main
    jmp main_loop
menu_settings:
    call clear_screen
    mov si, title_settings
    call print_string
    mov si, settings_options
    call print_string
    call wait_back
    call draw_main
    jmp main_loop

draw_main:
    call clear_screen
    mov si, main_title
    call print_string
    mov si, main_menu
    call print_string
    ret
clear_screen:
    mov ax, 0x0003
    int 0x10
    ret
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
wait_back:
    mov si, back_prompt
    call print_string
.wait:
    xor ah, ah
    int 0x16
    cmp al, 27
    je .done
    cmp al, 8
    je .done
    cmp al, 'b'
    je .done
    cmp al, 'B'
    jne .wait
.done:
    ret
reboot:
    int 0x19
.halt:
    cli
    hlt
    jmp .halt

main_title db 13,10,"==================================================",13,10
           db "              FLOPPY BOOT SUITE",13,10
           db "       BIOS Loader / Recovery Console",13,10
           db "==================================================",13,10,13,10,0
main_menu db " MAIN MENU",13,10,"  1. Boot and loader options",13,10
          db "  2. Disk tools and image options",13,10
          db "  3. Modules and submodules",13,10
          db "  4. System information / diagnostics",13,10
          db "  5. Help and keyboard controls",13,10
          db "  6. BIOS / CMOS settings reference",13,10
          db "  Q. Reboot",13,10,13,10,"Select an item by pressing its key.",13,10,0
title_boot db 13,10,"[ BOOT / LOADER OPTIONS ]",13,10
           db " Stage 1: BIOS boot sector",13,10," Stage 2: text UI shell",13,10
           db " Load address: 0000:8000",13,10," Mode: x86 16-bit real mode",13,10,0
title_disk db 13,10,"[ DISK TOOLS / IMAGE OPTIONS ]",13,10
           db " Target: 1.44 MB floppy image",13,10," Geometry: 80 cylinders, 2 heads, 18 sectors/track",13,10
           db " Disk-writing/cloning is not enabled in this UI.",13,10,0
title_modules db 13,10,"[ MODULE TREE ]",13,10
              db " Core",13,10,"  +-- BootManager / BIOSInit / Stage2Loader",13,10
              db "  +-- UserInterface / MainMenu / SubmenuRouter",13,10
              db "  +-- DiskServices (planned) / SectorReader / FAT12Parser",13,10
              db "  +-- Diagnostics / MemoryMap / BootReport",13,10,0
title_system db 13,10,"[ SYSTEM INFORMATION ]",13,10
             db " CPU mode: 16-bit real mode",13,10," UI: BIOS teletype console",13,10
             db " Boot sector: 512 bytes with 55 AA signature",13,10
             db " Stage 2 load window: 0000:8000",13,10
             db " FAT12 parser: planned",13,10,0
title_help db 13,10,"[ HELP / KEYBOARD ]",13,10
           db " Press 1-6 to open a section.",13,10," Press B, Backspace, or Escape to return.",13,10
           db " Press Q from the main menu to reboot.",13,10,0
title_settings db 13,10,"[ BIOS / CMOS SETTINGS REFERENCE ]",13,10
               db " Video: text mode 03h; keyboard: INT 16h",13,10
               db " Disk: BIOS INT 13h; retries are host-build defaults",13,10
               db " CMOS/RTC reads are diagnostic only; writes disabled",13,10
               db " JSON profiles describe defaults; not live hardware settings",13,10,0
boot_options db 13,10,"Stage 1 reads stage 2 using BIOS INT 13h.",13,10,0
disk_options db 13,10,"2880 sectors x 512 bytes = 1,474,560 bytes.",13,10,0
module_options db 13,10,"Core, UI, disk services, diagnostics, host tools.",13,10,0
system_options db 13,10,"Static build metadata only; full hardware tests are planned.",13,10,0
help_options db 13,10,"Keyboard shortcuts: B / Backspace / ESC.",13,10,0
settings_options db 13,10,"See config/boot_options.json and firmware/bios_profile.json.",13,10,0
back_prompt db 13,10,"Press ESC, Backspace, or B to return...",13,10,0
