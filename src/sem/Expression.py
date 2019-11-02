import lark
class ExpressionTree(lark.Tree):
	def __init__(self,name,children=[]):
		super().__init__(name,children)
		self.does_variate=True
class ExpressionInt(int):
	def __init__(self,*args,**kwargs):
		self.does_variate=False
	def __new__(cls,*args,**kwargs):
		return int.__new__(cls,int(*args,**kwargs))


class Expression():#custom trasnformer
	op_relacional_table={
		">" :lambda x,y:ExpressionInt(x> y),
		">=":lambda x,y:ExpressionInt(x>=y),
		"<" :lambda x,y:ExpressionInt(x< y),
		"<=":lambda x,y:ExpressionInt(x<=y),
		"==":lambda x,y:ExpressionInt(x==y),
		"!=":lambda x,y:ExpressionInt(x!=y)
	}
	soma_table={
		"+":lambda x,y:x+y,
		"-":lambda x,y:x-y
	}
	mult_table={
		"*":lambda x,y:x* y,
		"/":lambda x,y:x//y
	}
	def install(self,tree):
		if not isinstance(tree,lark.Tree):
			return tree
		args=[self.install(children) for children in tree.children]
		f=getattr(self,tree.data)
		if f==None:
			raise RuntimeError(f"Unexpected error {tree.data} not defined")
		ans=f(args)
		tree.expression=ans
		return ans
	def expressao(self,args):
		"""
		expressao: variavel ATTR expressao 
		| expressao_simples
		"""
		if len(args)==3:
			return ExpressionTree("=",[args[0],args[2]])
		return args[0]
	def expressao_simples(self,args):
		"""
		expressao_simples: soma_expressao op_relacional soma_expressao 
		| soma_expressao
		"""
		if len(args)==3:
			if isinstance(args[0],lark.Tree) or isinstance(args[2],lark.Tree):
				return ExpressionTree(args[1],[args[0],args[2]])
			return Expression.op_relacional_table[args[1]](args[0],args[2])
		return args[0]
	def soma_expressao(self,args):
		"""
		soma_expressao: soma_expressao soma termo 
		| termo
		"""
		if len(args)==3:
			if isinstance(args[0],lark.Tree) or isinstance(args[2],lark.Tree):
				return ExpressionTree(args[1],[args[0],args[2]])
			return Expression.soma_table[args[1]](args[0],args[2])
		return args[0]
	def termo(self,args):
		"""
		termo: termo mult fator 
		| fator
		"""
		if len(args)==3:
			if isinstance(args[0],lark.Tree) or isinstance(args[2],lark.Tree):
				return ExpressionTree(args[1],[args[0],args[2]])
			return Expression.mult_table[args[1]](args[0],args[2])
		return args[0]
	def soma(self,args):
		"""
		soma: SUMOP
		"""
		return args[0].value
	def op_relacional(self,args):
		"""
		op_relacional: RELOP
		"""
		return args[0].value
	def mult(self,args):
		"""
		mult: MULTOP
		"""
		return args[0].value
	def fator(self,args):
		"""
		fator: P_OPEN expressao P_CLOSE
		| variavel 
		| ativacao 
		| NUM
		"""
		if len(args)==3:
			return args[1]

		if isinstance(args[0],lark.Tree):
			return args[0]
		return ExpressionInt(args[0])
	def variavel(self,args):
		"""
		variavel: ID 
		| ID S_OPEN expressao S_CLOSE
		"""
		if len(args)==1:
			#TODO fix this hack
			ans=ExpressionTree("variavel")
			ans.var_name=args[0].value
			return ans
		return ExpressionTree("vetor",[args[2]])
	def ativacao(self,args):
		"""
		ativacao: ID P_OPEN argumentos P_CLOSE
		"""
		return ExpressionTree("ativacao",args[2])
	def argumentos(self,args):
		"""
		argumentos: lista_argumentos 
		| 
		"""
		if len(args)==0:
			return []
		return args[0]
	def lista_argumentos(self,args):
		"""
		lista_argumentos COMMA expressao 
		| expressao
		"""
		if len(args)==3:
			return args[0]+[args[2]]
		return [args[0]]
	
	
def is_head(tree):
	if tree==None: #safe switch
		return True
	tree=tree.parent
	while tree:
		if tree.data=="expressao":
			return False
		tree=tree.parent
	return True
def install_expression(tree):
	for subtree in tree.iter_subtrees():
		if not (subtree.data=="expressao" and is_head(subtree)):
			continue
		Expression().install(subtree)