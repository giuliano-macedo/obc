#!/usr/bin/env python3
from lex import TOKENS_DEFINITION
from lark import Lark
from lark.lexer import Lexer, Token
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
				yield Token(obj[0],obj[1])
def build_dot(tree,dot,complete=False):
	istoken=lambda obj:type(obj)==Token
	if complete:
		getData=lambda obj:f"\<{obj.type},{obj.value}\>" if istoken(obj) else obj.data
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

	lark = Lark(grammar,parser='lalr',lexer=Lex,start="programa")
	_input=json.load(args.input)
	tree = lark.parse(_input["tokens"])

	dot = Digraph()
	if args.complete_tree:
		dot.attr(rankdir="LR")
	build_dot(tree,dot,complete=args.complete_tree)
	dot.view('tree1', cleanup=True,quiet_view=True)
	print(tree.pretty())