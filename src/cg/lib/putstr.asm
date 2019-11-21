putstr:
	pop ecx				; some junk from call
	
	pop dword [putstr.str]

	push ecx			; putting it back, it must be important
	
	mov eax,[putstr.str]	;int* eax=putstr.str
	cmp dword [eax],0
	je putstr.endwhile0

	putstr.while0:		;	while(eax!=0){
		push eax		;	backup eax

		push dword [eax]
		call putchar

		pop eax

		add eax,4		;	eax+=4

		cmp dword [eax],0
		jne putstr.while0;	}
	putstr.endwhile0:
	ret