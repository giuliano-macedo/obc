from .TA import TA
import lark
def horn(exp):
	if isinstance(exp,int):
		return Horn([TA("=","t0",str(exp))],1)
	horn=Horn()
	horn.transform(exp)
	return horn

@lark.v_args(tree=True)
class Horn(lark.Transformer):
	def __init__(self,_list=list(),level=0):
		self.list=_list
		self.level=level
		for rule in TA.table.keys():
			setattr(self,rule,self.ari)

	def variavel(self,tree):
		return tree.var_name
	def ativacao(self,tree):
		raise RuntimeError(NotImplemented)
	def __default__(self,data,children,meta):
		raise RuntimeError(f"not implemented {data}")
	def ari(self, tree):
		self.level+=1
		t=f"t{self.level-1}"
		l,r=tree.children
		if tree.data=="=":
			ta1=TA("=",l,r)
			ta2=TA("=",t,l)
			self.list+=[ta1,ta2]
		else:
			ta=TA(tree.data,t,l,r)
			self.list.append(ta)
		return t



