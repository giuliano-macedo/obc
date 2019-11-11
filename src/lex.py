import graphviz
import os
import json
import lark
from utils import log_err

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

	("SUMOP",r"\+|\-"),
	("MULTOP",r"\*|\/"),
	("ARIOP",r"\+|\-|\*|\/"),
	("RELOP",r"<=|>=|==|\!=|<|>"),
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
def remove_comment(tokens):
	ans=True
	toremove=[]
	state=0
	for i,token in enumerate(tokens):
		if state==0:
			if token.type=="COMMENT_START":
				toremove.append(i)
				state+=1
		elif state==1:
			toremove.append(i)
			if token.type=="COMMENT_STOP":
				state=0
			
	if state==1:
		log_err(f"um comentário não tem fim!")
		ans=False
	multipop(tokens,toremove)
	return ans

def multipop(l,trm):
	# remove all indices in trm to remove from l
	for i in trm[::-1]:
		l.pop(i)
def remove_unknows(tokens):
	ans=True
	toremove=[]
	for i,token in enumerate(tokens):
		if token.type=="UNKNOW":
			log_err(f"token desconhecido {token.value}")
			ans=False
			toremove.append(i)
	multipop(tokens,toremove)
	return ans
def check_unknows_neighbors(tokens):
	# não podem ocorrer entre identificadores, números e palavras-chaves
	ans=True
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
						ans=False
						log_err("comentários não podem ocorrer no meio de identificadores, números e palavras-chaves")
				l,r=None,None
				state=0
	return ans
			
def make_dot_label(tokens):
	ans=[]
	for token in tokens:
		token_value="\\"+token.value if len(token.value)<=2 else token.value
		row=rf"\<{token.type},{token_value}\>"
		ans.append(row)
	return "{"+"|".join(ans)+"}"
def lex(f,no_output=False,show=False):
	b=True
	head=f"start:({'|'.join((k for k,v in TOKENS_DEFINITION))})*\n"
	body="\n".join((f"{k}:/{v}/" for k,v in TOKENS_DEFINITION))
	ignore="""
	%import common.WS
	%ignore WS\n"""
	grammar=head+body+ignore

	lexer=lark.Lark(grammar)
	code=f.read()
	try:
		ans=lexer.parse(code).children
	except Exception as e:
		log_err(f"erro léxico no arquivo {f.name}")
		raise e
	b&=remove_comment(ans)
	b&=remove_unknows(ans)
	b&=check_unknows_neighbors(ans)
	## el_out
	el_out = lambda tokens:",".join((token.type if token.type in {"ID","NUM"} else token.value for token in tokens))
	print("Saída:",el_out(ans))
	g=graph=graphviz.Graph()
	if not no_output:
		graph.node("",shape="record",label=make_dot_label(ans))
		graph.save("tokens.dot")
		graph.render("tokens",format="pdf",view=show,quiet_view=show)
		os.unlink("tokens")
	return b,f.name,ans
if __name__=="__main__":
	ok,tokens=lex(open("../samples/emails.c","r"),True)
	print(ok)