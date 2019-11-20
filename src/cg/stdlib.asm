section .text
global _start

%include "lib/putchar.asm"
%include "lib/putstr.asm"
%include "lib/putint.asm"
%include "lib/getchar.asm"
%include "lib/getint.asm"

_start:
	mov dword [SIZEOFINT],4

	call main

	mov eax, 1			; exit(
	mov ebx, 0			;   EXIT_SUCCESS
	int 0x80			; );

{code}

section .bss
	SIZEOFINT:	resb 4

	putint.n:	resb 4
	putint.flag:resb 1

	putstr.str:	resb 4

	putchar.c:	resb 4
	getchar.c:	resb 4
	getint.ans :	resb 4
	getint.fact :	resb 4
	getint.flag:	resb 1
	
	{symtable}