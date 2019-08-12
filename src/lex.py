#!/usr/bin/env python3
import argparse
import os
import json

st=lambda s:(s.upper(),s) #SIMPLE_TOKEN
TOKENS_DEFINITION=[
	st("if"),
	st("else"),
	st("int"),
	st("void"),
	st("return"),
	st("while"),

	("COMMENT_START",r"\/\*"),
	("COMMENT_STOP",r"\*\/"),

	("ARIOP",r"\+|\-|\*|\/"),
	("RELOP",r"<|<=|>|>=|==|\!="),
	("ATTR",r"="),
	("END_COMMAND",r"\;"),
	("COMMA",r"\,"),
	
	("P_OPEN",r"\("),
	("P_CLOSE",r"\)"),

	("S_OPEN",r"\["),
	("S_CLOSE",r"\]"),

	("B_OPEN",r"\{"),
	("B_CLOSE",r"\}"),

	("ID",r"[a-zA-Z]+"),
	("NUM",r"[0-9]+"),
	("UNKNOW",r"[^ \t\n]+"),
]
def clean_ox_mess():
	try:os.remove("parsetab.py")
	except Exception:pass
	try:os.remove("parser.out")
	except Exception:pass
def remove_comment(tokens):
	toremove=[]
	state=0
	for i,token in enumerate(tokens):
		if state==0:
			if token.type=="COMMENT_START":
				state+=1
		elif state==1:
			if token.type=="COMMENT_STOP":
				state=0
			else:
				toremove.append(i)
	if state==1:
		print(f"[ERRO] um comentário não tem fim!")
	multipop(tokens,toremove)

def multipop(l,trm):
	# remove all indices in trm to remove from l
	for i in trm[::-1]:
		l.pop(i)
def remove_unknows(tokens):
	toremove=[]
	for i,token in enumerate(tokens):
		if token.type=="UNKNOW":
			print(f"[ERRO] token desconhecido {token.value}")
			toremove.append(i)
	multipop(tokens,toremove)
def check_unknows_neighbors(tokens):
	# não podem ocorrer entre identificadores, números e palavras-chaves
	s=set(["IF","ELSE","VOID","RETURN","WHILE","ID","NUM"])
	state=0
	l,r=None,None
	for i,token in enumerate(tokens):
		if state==0:
			if token.type=="COMMENT_START":
				if i!=0:
					l=tokens[i-1]
					state+=1
				else:
					pass
		elif state==1:
			if token.type=="COMMENT_STOP":
				if i!=len(tokens)-1:
					r=tokens[i+1]
					if (l.type in s) and (l.type==r.type):
							print("[ERRO] comentários não podem ocorrer no meio de identificadores, números e palavras-chaves")
				l,r=None,None
				state=0
			
	
def lex(f):
	import ox
	lexer = ox.make_lexer(TOKENS_DEFINITION)
	code=f.read()
	try:
		ans=lexer(code)
	except Exception as e:
		print(f"[ERRO] erro léxico no arquivo {f.name}")
		clean_ox_mess()
		raise e
	clean_ox_mess()
	remove_comment(ans)
	remove_unknows(ans)
	check_unknows_neighbors(ans)
	return ans
if __name__=="__main__":
	def el_out(tokens):
		s=set(("ID","NUM"))
		return ",".join((token.type if token.type in s else token.value for token in tokens))

	parser=argparse.ArgumentParser()
	parser.add_argument("input",type=argparse.FileType('r'))
	parser.add_argument("-o","--output",type=argparse.FileType('w'),default="tokens.json")
	args=parser.parse_args()

	out=lex(args.input)
	print("Saída:",el_out(out))
	
	args.output.write("{\"tokens\":[\n")
	json_str=lambda s:json.dumps(s,ensure_ascii=False)
	for token_name,token_value in ((token.type,token.value) for token in out):
		args.output.write(f"\t[{json_str(token_name)},{json_str(token_value)}],\n")
	if len(out)!=0:
		args.output.seek(args.output.tell()-2)
	args.output.write("\n]}")
