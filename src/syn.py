#!/usr/bin/env python3
from lex import TOKENS_DEFINITION
from lark import Lark
from lark.lexer import Lexer, Token
from lark.grammar import Terminal
from graphviz import Digraph
import json
import argparse

TOKENS_NAMES=[t[0] for t in TOKENS_DEFINITION]

def forgot_comma(code,tokens):
	"você esqueceu do ',' ?"
	pass
def forgot_semicolomn(code,tokens):
	"você esqueceu do ';' ?"
	for i,line in enumerate(code.split("\n")):
		line=line.strip()
		if len(line)==0:
			continue
		if line[-1] in set("{}(),/*"):
			continue
		if line[-1]!=";":
			old_line=line
			new_line=line+";"
			index=tokens_in_line(tokens,i)[-1]

			last_token=tokens[index]
			last_token_len=len(last_token[1])
			tokens.insert(index+1,
				("END_COMMAND",";",
					i+1,
					last_token[3]+last_token_len,
					last_token[4]+last_token_len
				)
			)
			yield old_line,new_line
def tokens_in_line(tokens,line):
	return [i for i,token in enumerate(tokens) if token[2]==line+1]
def search_and_replace(code,tokens):
	hooks=[
		# forgot_comma,
		forgot_semicolomn
	]
	for rule_func in hooks:
		for ans in rule_func(code,tokens):
			# if ans==None:
			# 	continue
			old_line,new_line=ans
			print(f"[AVISO] linha '{old_line}' considerada como '{new_line}', ({rule_func.__doc__})")

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


if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument("input",type=argparse.FileType('r'),default="tokens.json",nargs='?')
	parser.add_argument("-o","--output",type=argparse.FileType('w'),default="tree1.json")
	parser.add_argument("-C","--complete-tree", action='store_true')
	args=parser.parse_args()

	lark = Lark(grammar,parser='lalr',lexer=Lex,start="programa",propagate_positions=True)
	_input=json.load(args.input)
	search_and_replace(open(_input["filename"]).read(),_input["tokens"])
	tree = lark.parse(_input["tokens"])

	dot = Digraph()
	if args.complete_tree:
		dot.attr(rankdir="LR")
	build_dot(tree,dot,complete=args.complete_tree)
	dot.view('tree1', cleanup=True,quiet_view=True)
	print(tree.pretty())