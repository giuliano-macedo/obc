putint:
	pop ecx				; address of return from call
	
	pop dword [putint.n]

	push ecx			; putting it back, it is important

	push dword 0		;$
	push dword 10		;\n

	mov eax,[putint.n]			;eax=n
	mov byte [putint.flag],0	;flag=0

	cmp eax,0
	jge putint.endif0
	putint.if0:
		mov byte [putint.flag],1	;flag=1
		imul eax,-1
	putint.endif0:

	putint.dowhile0:		;do{
		
		xor edx,edx 		;edx=0
		mov dword ecx,10
		div ecx				;eax//=10
		add edx,'0'
		push dword edx		;push (eax%10)+'0'
		
		cmp dword eax,0	
		jne putint.dowhile0
	putint.enddowhile0:		;}while(eax!=0)


	cmp byte [putint.flag],1
	jne putint.endif1
	putint.if1:
		push dword "-"
	putint.endif1:


	putint.while0:			;while(true){
		mov eax,[esp]		;eax=*stack.top
		cmp dword eax,0 	;if (eax==0) break
		jz putint.endwhile0
		call putchar		;consume stack and print
		jmp putint.while0
	putint.endwhile0:		;}



	; pop dword eax
	add esp,4
	ret