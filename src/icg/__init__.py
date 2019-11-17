from .Transformer import Transformer
from .TA import TA,Label
import lark

def flatten(l):
	# https://stackoverflow.com/a/12474246/5133524
	return sum(map(flatten,l),[]) if isinstance(l,list) else [l]

def tabify(l):
	for i,elem in enumerate(l):
		if isinstance(elem,str):
			l[i]="\t"+elem
		else:
			tabify(elem)

@lark.v_args(tree=True)
class Tac2File(lark.Transformer):
	def __init__(self,fname,*args,**kwargs):
		self.f=open(fname,"w")
		super().__init__(*args,**kwargs)
		for rule in TA.table.values():
			setattr(self,rule,self.ta)
	def tac(self,tree):
		self.f.write(f"<max_level={tree.max_level}>\n")
		for line in flatten(tree.children):
			self.f.write(line)
		self.f.close()
	def label(self,tree):
		tabify(tree.children)
		return [f"{tree.name}:\n"]+tree.children
	def ta(self,tree):
		return tree.to_str()+"\n"
def fix_var_name(symtable,ta_list,scope=None):
	def add_scope_if_possible(scope,var):
		if var==None:
			return var
		entry=symtable.get("."+scope,var)
		if entry==None:
			return var
		else:
			if entry.scope!="":
				return entry.scope[1:]+"."+entry.name
			else:
				return entry.name
	if scope==None:
		for inst in ta_list:
			if isinstance(inst,Label):
				fix_var_name(symtable,inst.children,inst.name)
		return
	for inst in ta_list:
		if isinstance(inst,Label):
			inst.name=scope+"."+inst.name
			fix_var_name(symtable,inst.children,scope)
		else:
			inst.arg1=add_scope_if_possible(scope,inst.arg1)
			inst.arg2=add_scope_if_possible(scope,inst.arg2)
			inst.arg3=add_scope_if_possible(scope,inst.arg3)

def icg(tree,symtable):
	tac_tree=Transformer(symtable).transform(tree)
	fix_var_name(symtable,tac_tree.children)
	fname="tac.txt"
	Tac2File(fname).transform(tac_tree)
	exit()
	# return True