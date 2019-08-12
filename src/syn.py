#!/usr/bin/env python3
from lex import TOKENS_DEFINITION
from lark import Lark
from lark.lexer import Lexer, Token
from graphviz import Digraph
import json
import argparse

TOKENS_NAMES=[t[0] for t in TOKENS_DEFINITION]

class Lex(Lexer):
	def __init__(self, lexer_conf):
		pass

	def lex(self, data):
		for obj in data:
			if obj[0] not in {"COMMENT_START", "COMMENT_STOP"}:
				yield Token(obj[0],obj[1])
def build_dot(tree,dot):
	h=str(id(tree))
	getData=lambda obj:obj if type(obj)==Token else obj.data
	label=getData(tree) if type(tree)==Token else f"<<font face=\"boldfontname\">{getData(tree)}</font>>"
	dot.node(h,label=label)
	if type(tree) == Token:
		return 
	for children in tree.children:
		dot.edge(h,str(id(children)))
		build_dot(children,dot)
with open("grammar.lark") as f:
	grammar=f.read() + f"\n%declare {' '.join(TOKENS_NAMES)}"


if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument("input",type=argparse.FileType('r'),default="tokens.json",nargs='?')
	parser.add_argument("-o","--output",type=argparse.FileType('w'),default="tree1.json")
	args=parser.parse_args()

	lark = Lark(grammar,parser='lalr',lexer=Lex)
	_input=json.load(args.input)
	tree = lark.parse(_input["tokens"])

	dot = Digraph()
	build_dot(tree,dot)
	dot.render('tree1.dot', view=True)
	print(tree.pretty())