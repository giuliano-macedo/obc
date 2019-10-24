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
	value=put_token_dict[to_add_name]
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
	print(f"[AVISO] linha '{old_line}' considerada como '{new_line}', número da linha :{line}")
def is_block(tokens,start):
	#TODO
	return False
def find_block(tokens,start):
	pass
def remove_line_or_block(tokens,line):
	ans=[line]
	line_start_index=next(i for i,token in enumerate(tokens) if token[2]==line)
	if is_block(tokens,line_start_index):
		ans+=list(find_block(tokens,line_start_index))
	ans_set=set(ans)
	for i in range(len(tokens)-1,-1,-1):
		if tokens[i][2] in ans_set:
			# print("removing ",tokens[i])
			tokens.pop(i)
	return ans

if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument("input",type=argparse.FileType('r'),default="tokens.json",nargs='?')
	parser.add_argument("-o","--output",type=argparse.FileType('w'),default="tree1.json")
	parser.add_argument("-C","--complete-tree", action='store_true')
	args=parser.parse_args()

	lark = Lark(grammar,parser='lalr',lexer=Lex,start="programa",propagate_positions=True)
	_input=json.load(args.input)
	tokens=_input["tokens"]
	code=open(_input["filename"]).read()
	code_splitted=code.split("\n")
	while True:
		if len(tokens)==0:
			print("[ERRO]impossivel recuperar de erros")
			exit(-1)
		did_parse,e=try_parse(lark,tokens)
		if did_parse:
			tree=e
			break
		modified_tokens=tokens.copy()
		token_index=next(i for i,token in enumerate(tokens) if token[2]==e.line and token[3]==e.column)
		#----------------try to put expected token----------------
		sucess=False
		expecteds=[expected for expected in e.expected if expected not in {"ID","NUM","SUMOP","RELOP","ARIOP","MULTOP"}]
		expecteds.sort() #replicability
		if "COMMA" in expecteds: #PREFERENCE TO COMMA
			expecteds.insert(0,expecteds.pop(expecteds.index("COMMA")))
		for expected in expecteds:
			# print(f"trying to put {expected}")
			index_added=put_token(modified_tokens,token_index,expected)
			stop,e2=try_parse(lark,modified_tokens)
			if stop or not (e.line<=e2.line<=(e.line+1)):
				tokens=modified_tokens
				inform_line_changed(tokens,code_splitted,e.line)
				sucess=True
				break
			#removed last added token
			modified_tokens.pop(index_added)
		if sucess:
			continue
		#----------------remove whole line or block----------------
		removed_lines=remove_line_or_block(tokens,e.line)
		print(f"[AVISO] a linha a seguir foi ignoradas por erro sintáxico:")
		for line in removed_lines:
			print(repr(code_splitted[line-1].strip()),line)
	dot = Digraph()
	if args.complete_tree:
		dot.attr(rankdir="LR")
	build_dot(tree,dot,complete=args.complete_tree)
	dot.view('tree1', cleanup=True,quiet_view=True)
	# print(tree.pretty())