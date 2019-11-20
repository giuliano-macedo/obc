getint:
	
	mov dword [getint.fact],1		;fact=1
	mov dword [getint.ans],0	;ans=0

	getint.dowhile0:	;do{
		call getchar
		pop dword edx	;edx=getchar()

		cmp edx,10		;if(edx=='\n')break
		je getint.enddowhile0

		sub edx,'0'				;edx-='0'

		mov eax,[getint.fact]	;eax=fact

		mul edx					;eax*=edx

		mov ebx,[getint.ans]	;ebx=ans
		add ebx,eax				;ebx+=eax

		mov [getint.ans],ebx	;ans+=getchar()*fact

		mov eax,[getint.fact]	;fact*=10
		mov ebx,10
		mul ebx
		mov [getint.fact],eax

		jmp getint.dowhile0
	getint.enddowhile0:	;}while(*stack.top!=0)

	pop edx

	push dword [getint.ans]

	push edx
	ret