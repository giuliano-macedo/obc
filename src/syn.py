#!/usr/bin/env python3
from lex import TOKENS_DEFINITION
from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
from lark.grammar import Terminal
from graphviz import Digraph
import json
import argparse

TOKENS_NAMES=[t[0] for t in TOKENS_DEFINITION]

def log_err(msg):
	print("[\033[31mERRO \033[0m]",msg)
def log_war(msg):
	print("[\033[35mAVISO\033[0m]",msg)

class Lex(Lexer):
	def __init__(self, lexer_conf):
		pass
	def lex(self, data):
		for obj in data:
				yield Token(obj[0],obj[1],line=obj[2],column=obj[3],pos_in_stream=obj[4])
def build_dot(tree,dot,complete=False):
	istoken=lambda obj:type(obj)==Token
	if complete:
		getData=lambda obj:rf"\<{obj.type},{obj.value}\>" if istoken(obj) else obj.data
	else :
		getData=lambda obj:obj if istoken(obj) else obj.data
	h=str(id(tree))
	label=getData(tree) if istoken(tree) else f"<<font face=\"boldfontname\">{getData(tree)}</font>>"
	dot.node(h,label=label)
	if istoken(tree):
		return 
	for children in tree.children:
		dot.edge(h,str(id(children)))
		build_dot(children,dot,complete)
with open("grammar.lark") as f:
	grammar=f.read() + f"\n%declare {' '.join(TOKENS_NAMES)}"

def fatal_err(code,err):
	code_splitted=code.split("\n")
	print(f"erro fatal na linha:",repr(code_splitted[err.line-1].strip()))
	print("\t",f"número da linha:{err.line} coluna:{err.column}")
	print(f"era esperado um dos seguintes tokens {err.expected}")
	exit(-1)
def informe_syntax_err(err,line_str):
	log_err(f"na linha {repr(line_str)}")
	print("\t"+f"número da linha:{err.line} coluna:{err.column}")
	print("\t"+f"era esperado um dos seguintes tokens {err.expected}")

def try_parse(parser,tokens):
	"""
	try parse using lark parser
	Returns:
		tuple (did_parsed,tree/err)
	"""
	try:
		tree = lark.parse(tokens)
	except UnexpectedToken as e:
		return (False,e)
	return (True,tree)
put_token_dict={k:v.replace("\\","") for k,v in TOKENS_DEFINITION if k not in {"ID","NUM"}}
def put_token(tokens,i,to_add_name):
	global put_token_dict 
	last_token=tokens[i]
	last_token_len=len(last_token[1])
	value=put_token_dict.get(to_add_name)
	if value==None:
		return -1
	tokens.insert(i,(
		to_add_name,
		value,
		last_token[2],
		last_token[3]+last_token_len,
		last_token[4]+last_token_len	
	))
	return i
def get_line_from_tokens(tokens,line):
	return " ".join((token[1] for token in tokens if token[2]==line))
def inform_line_changed(tokens,code_splitted,line):
	old_line=code_splitted[line-1].strip()
	new_line=get_line_from_tokens(tokens,line)
	log_war(f"linha '{old_line}' considerada como '{new_line}', número da linha :{line}")
def remove_line(tokens,line):
	for i in range(len(tokens)-1,-1,-1):
		if tokens[i][2] ==line:
			# print("removing ",tokens[i])
			tokens.pop(i)

if __name__ == '__main__':
	def try_to_put_expected_token(): #TODO GLOBALS
		global tokens
		sucess=False
		expecteds=[expected for expected in e.expected if expected not in {"ID","NUM","SUMOP","RELOP","ARIOP","MULTOP","$END"}]
		expecteds.sort() #replicability
		if "COMMA" in expecteds: #PREFERENCE TO COMMA
			expecteds.insert(0,expecteds.pop(expecteds.index("COMMA")))
		for expected in expecteds:
			# print(f"trying to put {expected}")
			index_added=put_token(modified_tokens,token_index,expected)
			if index_added==-1:
				continue
			stop,e2=try_parse(lark,modified_tokens)
			if stop or not (e.line<=e2.line<=(e.line+1)):
				tokens=modified_tokens
				inform_line_changed(tokens,code_splitted,e.line)
				sucess=True
				break
			#removed last added token
			modified_tokens.pop(index_added)
		return sucess
	parser=argparse.ArgumentParser()
	parser.add_argument("input",type=argparse.FileType('r'),default="tokens.json",nargs='?')
	parser.add_argument("-o","--output",type=argparse.FileType('w'),default="tree1.json")
	parser.add_argument("-C","--complete-tree", action='store_true')
	parser.add_argument("-f","--force-parse", action='store_true')
	parser.add_argument("-N","--dont-try-to-fix-errs", action='store_false')
	args=parser.parse_args()

	lark = Lark(grammar,parser='lalr',lexer=Lex,start="programa",propagate_positions=True)
	_input=json.load(args.input)
	tokens=_input["tokens"]
	if len(tokens)==0:
		log_err("programa vazio")
		exit(-1)
	code=open(_input["filename"]).read()
	code_splitted=code.split("\n")
	failed=False
	while True:
		if len(tokens)==0:
			break
		did_parse,e=try_parse(lark,tokens)
		if did_parse:
			tree=e
			break
		modified_tokens=tokens.copy()
		token_index=next(i for i,token in enumerate(tokens) if token[2]==e.line and token[3]==e.column)
		#----------------try to put expected token----------------
		if args.dont_try_to_fix_errs and try_to_put_expected_token():
			continue
		#----------------remove whole line----------------
		remove_line(tokens,e.line)
		informe_syntax_err(e,code_splitted[e.line-1].strip())
		failed=True
	if failed and not args.force_parse:
		print("Houve um erro sintático, portanto nenhuma arvore foi gerada")
		exit(-1)
	dot = Digraph()
	if args.complete_tree:
		dot.attr(rankdir="LR")
	build_dot(tree,dot,complete=args.complete_tree)
	dot.view('tree1', cleanup=True,quiet_view=True)
	# print(tree.pretty())