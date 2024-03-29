from .TA import TA
import lark
def horn(exp):
	"""
	sem.Expression TA parser
	"""
	if isinstance(exp,int):
		return Horn([TA("=",Temporary_Variable(0),str(exp))],1)
	if exp.data=="variavel":
		return Horn([TA("=",Temporary_Variable(0),str(exp.var_name))],1)
	horn=Horn()
	horn.transform(exp)
	return horn
class Temporary_Variable(str):
	def __new__(cls,i,is_vec=False):
		obj=str.__new__(cls,f"t{i}")
		obj.i=i
		obj.is_vec=is_vec
		return obj
	# def __str__(self):
	# 	return self
@lark.v_args(tree=True)
class Horn(lark.Transformer):
	def __init__(self,_list=None,level=0):
		self.list=_list if _list else []
		self.level=level
		for rule in TA.table.keys():
			setattr(self,rule,self.ari)
	def vetor(self,tree):
		self.level+=1
		t=Temporary_Variable(self.level-1,is_vec=True)
		u=tree.var_name
		i=tree.children[0]
		ta=TA("index",t,u,i)
		self.list.append(ta)
		return t
	def variavel(self,tree):
		return tree.var_name
	def ativacao(self,tree):
		for arg in tree.children:
			self.list.append(TA("arg",arg))
		self.list.append(TA("call",tree.var_name))
		self.level+=1
		t=Temporary_Variable(self.level-1)
		self.list.append(TA("get_ret",t))
		return t
	def __default__(self,data,children,meta):
		raise RuntimeError(f"not implemented {data}")
	def ari(self, tree):
		self.level+=1
		t=Temporary_Variable(self.level-1)
		l,r=tree.children
		if tree.data=="=":
			#check if the variable that is beign set is vector, if it is, add set_at_index instruction
			#----------------------------------------------------------------------------------------
			if isinstance(l,Temporary_Variable) and l.is_vec:
				index_t_index=next((i for i,ta in enumerate(self.list) if ta.arg1==l and ta.op=="index"),None)
				if index_t_index==None:
					raise RuntimeError("Unexpected error")
				index_t=self.list.pop(index_t_index)
				u=index_t.arg2
				i=index_t.arg3
				ta1=TA("set_at_index",u,i,r)
				ta2=TA("=",t,l)
				self.list+=[ta1,index_t,ta2]
			else:
				ta1=TA("=",l,r)
				ta2=TA("=",t,l)
				self.list+=[ta1,ta2]
		else:
			ta=TA(tree.data,t,l,r)
			self.list.append(ta)
		return t



