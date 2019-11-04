def myrepr(v):
	if isinstance(v,str):
		if v=="":
			return "ε"
		return '"'+v+'"'
	if isinstance(v,list):
		return str(["int[]" if a.is_vector() else "int" for a in v])
	return repr(v)
from .Symtable import Symtable
from .Visitor import Visitor
from .Expression import install_expression
from functools import partial
from utils import log_err,log_war
import graphviz
import lark
def build_dot_expression(exp_tree,dot):
	h=str(id(exp_tree))
	if isinstance(exp_tree,int) or isinstance(exp_tree,str):
		dot.node(h,label=str(exp_tree),shape="box")
		return
	elif isinstance(exp_tree,list):
		dot.node(h,label="list",shape="box")
		for element in exp_tree:
			build_dot_expression(element,dot)
		return
	label=str(exp_tree.data)
	if getattr(exp_tree,"var_name",None)!=None:
		label+="\nvar_name="+repr(exp_tree.var_name)
	dot.node(h,label=label,shape="box")
	for i,children in enumerate(exp_tree.children):
		r=str(id(children))
		dot.edge(h,r,label=["left","right"][i] if len(exp_tree.children)==2 else "")
		build_dot_expression(children,dot)
def build_dot(tree,dot,complete=False):
	istoken=lambda obj:isinstance(obj,lark.Token)
	if complete:
		getData=lambda obj:rf"\<{obj.type},{obj.value}\>" if istoken(obj) else obj.data
	else :
		getData=lambda obj:obj if istoken(obj) else obj.data
	h=str(id(tree))
	if istoken(tree):
		dot.node(h,label=getData(tree))
		return 

	label=tree.data
	if tree.data in {"declaracao_selecao","declaracao_iteracao"} and getattr(tree,"label",None)!=None:
		label+="\n"+f"label={repr(tree.label)}"
	elif tree.data in {"declaracao_variaveis","declaracao_funcoes"} and getattr(tree,"entry",None)!=None:
		label+="\n"+"\n".join(f"{k}={myrepr(v)}" for k,v in vars(tree.entry).items())
	dot.node(h,label=label)
	if tree.data in {"expressao","expressao_simples","soma_expressao","termo","soma","op_relacional","mult","fator","variavel","ativacao","argumentos","lista_argumentos","install_expression"}:
		dot.edge(h,str(id(tree.expression)),label="expression",color="red")
		build_dot_expression(tree.expression,dot)
	for children in tree.children:
		r=str(id(children))
		dot.edge(h,r)
		if not istoken(children):
			dot.edge(r,h,color="red",label="parent")
		build_dot(children,dot,complete)
def shape_tree(subtree,parent=None): 
	"""
	adds parent attribute to tree nodes
	"""
	if not isinstance(subtree,lark.Tree):
		return
	subtree.parent=parent
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
	install_expression(tree)
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
			b=False
			log_err(f"a última função declarada{str1} tem o nome main,{str2} é de tipo void e{str3} tem argumentos")
	get_msg=lambda entry:f"{'função' if entry.is_function() else 'variável'} {repr(entry.name)}"
	for entry in symtable.table.values():
		
		if not entry.referenced:
			onwarn(
				code_splitted,
				entry.line,
				get_msg(entry)+" definida porém nunca utilizada"
			)
		elif entry.is_var() and not entry.initialized:
			onwarn(
				code_splitted,
				entry.line,
				get_msg(entry)+" não foi inicializada"
			)
		if entry.is_function() and entry.type!="void" and not entry.does_return:
			onerr(
				code_splitted,
				entry.line,
				get_msg(entry)+" não retorna valor !"
			)
			b=False

	if not no_output:
		symtable_graph=symtable.to_graphviz()
		symtable_graph.save("symtable.dot")
		symtable_graph.render('symtable',format="pdf", cleanup=True,view=show,quiet_view=show)

		dot = graphviz.Digraph(strict=True)
		if complete_tree:
			dot.attr(rankdir="LR")
		build_dot(tree,dot,complete=complete_tree)
		dot.save("semantic_tree.dot")
		dot.render('semantic_tree',format="pdf", cleanup=True,view=show,quiet_view=show)

	return b,tree,symtable