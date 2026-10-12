; NASM pseudo-object conventions for 16-bit real-mode projects.
; This is a compile-time convention, not native language OOP.
%ifndef FLOPPY_OOP_MACROS_INC
%define FLOPPY_OOP_MACROS_INC 1
; Declare a layout with STRUC / ENDSTRUC; instantiate with ISTRUC / IEND.
; Example:
; STRUC Counter
;   .value: resw 1
;   .step:  resw 1
; ENDSTRUC
; counter_a: istruc Counter
;   at Counter.value, dw 0
;   at Counter.step, dw 1
; iend
; A method convention may pass DS:BX -> object. Document clobbers and return values.
%endif
