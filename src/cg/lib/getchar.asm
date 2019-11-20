getchar:
	
	mov eax, 3			; read(
	mov ebx, 0			;   stdin,
	mov ecx, getchar.c	;   c,
	mov edx, 1			;   1
	int 0x80			; );

	pop edx

	push dword [getchar.c]

	push edx
	ret