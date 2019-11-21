putchar:
	pop ecx				; some junk from call
	
	pop eax
	mov byte [putchar.c],al

	push ecx			; putting it back, it must be important

	mov eax, 4			; write(
	mov ebx, 1			;   stdout,
	mov ecx, putchar.c	;   c,
	mov edx, 1			;   1
	int 0x80			; );
	ret