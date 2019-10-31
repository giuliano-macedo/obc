from .Symtable import Symtable
from .Visitor import Visitor
from functools import partial
from utils import log_err,log_war
import lark
def shape_tree(subtree,parent=None):
	if not isinstance(subtree,lark.Tree):
		return
	subtree.parent=parent
	subtree.extra={}
	for children in subtree.children:
		shape_tree(children,subtree)
def onerr(code_splitted,line,msg):
	line_str=code_splitted[line-1].strip()
	log_err(f"na linha {repr(line_str)} número da linha: {line}")
	print(f"\t{msg}")
def onwarn(code_splitted,line,msg):
	line_str=code_splitted[line-1].strip()
	log_war(f"na linha {repr(line_str)} número da linha: {line}")
	print(f"\t{msg}")
def sem(code_splitted,fname,tree,complete_tree,no_output,show):
	b=True
	shape_tree(tree)
	symtable=Symtable()
	visitor=Visitor(symtable,onerr=partial(onerr,code_splitted),onwarn=partial(onwarn,code_splitted))
	visitor.visit_top_down(tree)
	b&=visitor.ok
	print("-"*16,"SYMTABLE","-"*16)
	print(*(f"{k}->{repr(v)}" for k,v in symtable.table.items()),sep="\n")
	exit()
	# return b,ans,symtable