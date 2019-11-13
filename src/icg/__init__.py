from .Transformer import Transformer
from .TA import TA
import lark

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
		# https://stackoverflow.com/a/12474246/5133524
		flatten=lambda l: sum(map(flatten,l),[]) if isinstance(l,list) else [l]
		for line in flatten(tree.children):
			self.f.write(line)
		self.f.close()
	def label(self,tree):
		tabify(tree.children)
		return [f"{tree.name}:\n"]+tree.children
	def ta(self,tree):
		return tree.to_str()+"\n"
def icg(tree,symtable):
	tac_tree=Transformer(symtable).transform(tree)
	fname="tac.txt"
	Tac2File(fname).transform(tac_tree)
	exit()
	# return True