section .text
global _start
_start:
	mov dword [SIZEOFINT],4

	; call .main

	; push dword 13
	; call .putint

	push dword 'a'
	call putchar
	push dword 10
	call putchar

	mov byte [str+ 0],"h"
	mov byte [str+ 4],"e"
	mov byte [str+ 8],"l"
	mov byte [str+ 12],"l"
	mov byte [str+ 16],"o"
	mov byte [str+ 20]," "
	mov byte [str+ 24],"w"
	mov byte [str+ 28],"o"
	mov byte [str+ 32],"r"
	mov byte [str+ 36],"l"
	mov byte [str+ 40],"d"
	mov byte [str+ 44],10
	mov byte [str+ 48],0
	push str
	call putstr

	push dword 4242130
	call putint

	call getint
	
	pop dword eax
	
	push dword eax
	push dword eax
	call putint
	
	call putchar
	push dword 10
	call putchar

	call getchar
	
	pop dword eax
	
	push dword eax
	push dword eax
	call putint
	
	call putchar
	push dword 10
	call putchar


	mov eax, 1			; exit(
	mov ebx, 0			;   EXIT_SUCCESS
	int 0x80			; );

%include "putchar.asm"
%include "putstr.asm"
%include "putint.asm"
%include "getchar.asm"
%include "getint.asm"

; .putint:

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
	
	str:		resb 52	;13*4
	;{symtable}