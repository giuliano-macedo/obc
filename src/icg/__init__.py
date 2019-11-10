from .Transformer import Transformer
from .TA import TA
import lark

def tabify(l):
	return ["\t"+line for line in l]

@lark.v_args(tree=True)
class Tac2File(lark.Transformer):
	def __init__(self,fname,*args,**kwargs):
		self.f=open(fname,"w")
		super().__init__(*args,**kwargs)
		for rule in TA.table.values():
			setattr(self,rule,self.ta)
	def tac(self,tree):
		self.f.write(f"<max_level={tree.max_level}>\n")
		for children in tree.children:
			for line in children:
				self.f.write(line)
		self.f.close()
	def label(self,tree):
		return [f"{tree.name}:\n"]+tabify(tree.children)
	def ta(self,tree):
		return tree.to_str()+"\n"
def icg(tree,symtable):
	tac_tree=Transformer(symtable).transform(tree)
	fname="tac.txt"
	Tac2File(fname).transform(tac_tree)
	exit()
	# return True