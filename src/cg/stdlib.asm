section .text
global _start

%include "cg/lib/putchar.asm"
%include "cg/lib/putstr.asm"
%include "cg/lib/putint.asm"
%include "cg/lib/getchar.asm"
%include "cg/lib/getint.asm"

;stdlib	
;-------------------------------------------------------

_start:
	mov dword [SIZEOFINT],4

	call main

	mov eax, 1			; exit(
	mov ebx, 0			;   EXIT_SUCCESS
	int 0x80			; );
;user
;-------------------------------------------------------
{code}

section .bss
;stdlib	
;-------------------------------------------------------
	SIZEOFINT:	resb 4

	putint.n:	resb 4
	putint.flag:resb 1

	putstr.str:	resb 4

	putchar.c:	resb 4
	getchar.c:	resb 4
	getint.ans :	resb 4
	getint.fact :	resb 4
	getint.flag:	resb 1
;user
;-------------------------------------------------------
{symtable}