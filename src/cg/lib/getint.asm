getint:
	
	mov dword [getint.fact],1		;fact=1
	mov dword [getint.ans],0		;ans=0

	push dword 0	;$

	break:
	getint.while0:	;while(true){
		call getchar
		pop dword edx	;edx=getchar()

		cmp edx,10		;if(edx=='\n')break
		je getint.endwhile0
		push dword edx
		jmp getint.while0
	getint.endwhile0:	;}

	getint.l0:
		
		pop dword edx
		cmp edx,0
		je getint.end
		cmp edx,'-'
		je getint.special

		sub edx,'0'				;eax=fact*(*stack.top)
		mov dword eax,[getint.fact]
		mul edx

		mov dword ebx,[getint.ans] 	;ans+=eax
		add ebx,eax
		mov [getint.ans],ebx

		mov dword eax,[getint.fact]			;fact*=10
		mov ebx,10
		mul ebx
		mov dword [getint.fact],eax

		jmp getint.l0


	getint.special:
		mov byte [getint.flag],1
		pop dword edx
		cmp edx,0
		je getint.end
		jmp getint.special
	getint.end:
		cmp byte [getint.flag],1
		jne getint.nflag
		mov dword eax,[getint.ans]	;ans*=-1
		mov ebx,-1
		mul ebx
		mov dword [getint.ans],eax
	getint.nflag:

	pop edx

	push dword [getint.ans]

	push edx
	ret