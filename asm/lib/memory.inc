; DS:SI source, ES:DI destination, CX byte count.
%ifndef FLOPPY_LIB_MEMORY_INC
%define FLOPPY_LIB_MEMORY_INC 1
memory_copy:
    cld
    rep movsb
    ret
memory_fill:
    cld
    rep stosb
    ret
%endif
