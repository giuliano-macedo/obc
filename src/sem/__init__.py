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
	all_functions=[entry for entry in symtable.table.values() if entry.is_function()]
	last_function=None
	try:
		last_function=all_functions[-1]
	except IndexError:
		log_err("Nenhuma função foi declarada!, função void main(void) precisa ser declarada!")
		b=False
	if last_function:
		is_main=last_function.name=="main"
		is_void=last_function.type=="void"
		does_have_args=last_function.args!=[]

		if (is_main,is_void,does_have_args)!=(True,True,False):
			str1="" if is_main else " não"
			str2="" if is_void else " não"
			str3="" if does_have_args else " não"
			b==False
			log_err(f"a última função declarada{str1} tem o nome main,{str2} é de tipo void e{str3} tem argumentos")
		
	print("-"*16,"SYMTABLE","-"*16)
	print(*(f"{k}->{repr(v)}" for k,v in symtable.table.items()),sep="\n")
	exit()
	# return b,ans,symtable