from collections import deque
import lark
class Symtable:
	class Entry:
		"""
		Symtable entry

		Attributes:
			type (str): variable or function type
			scope (str): name of parent function, "" if it's root of the code
			size (int): size of the vector, -1 if it's single variable, None if undefined
			referenced (bool): if the variable has changed
			initialized (bool): if the variable was initialized
			args (list): if variable this should be None, if function, it must have the list of entries that represents its arguments
			line (int): line where the variable or function was defined
		"""
		def __init__(self,name,_type,scope,size,referenced,initialized,args,line):
			self.name=name
			self.type=_type
			self.scope=scope
			self.size=size
			self.referenced=referenced
			self.initialized=initialized
			self.args=args
			self.line=line

		def is_function(self):
			return self.no_args!=None
		def is_var(self):
			return not self.is_function()
		def is_vector(self):
			return self.size!=-1
		def __str__(self):
			return repr(self)
		def __repr__(self):
			kwargs=",".join(f"{k}={repr(v)}" for k,v in vars(self).items())
			return f"Symtable.Entry({kwargs})"



	def __init__(self):
		self.table={}
	def add_variable(self,name,_type,scope,line):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=Symtable.Entry(
			name=name,
			_type=_type,
			scope=scope,
			size=-1,
			referenced=False,
			initialized=False,
			args=None,
			line=line
		)
	def add_function(self,name,_type,scope,line,args):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=Symtable.Entry(
			name=name,
			_type=_type,
			scope=scope,
			size=-1,
			referenced=False,
			initialized=True,
			args=args,
			line=line
		)
	def __getitem__(self,k):
		return self.table[k]
	def get(self,scope,k):
		if isinstance(scope,lark.Tree):
			return self.table.get((Symtable.get_scope(scope)+"."+k))
		return self.table.get((scope+"."+k))
	def get_scope(tree):
		important=[]
		
		while tree:
			if tree.data=="declaracao_funcoes":
				important.append(tree.children[1].value)
			if tree.data=="programa":
				important.append("")
			tree=tree.parent
		return ".".join(important[::-1])
class Visitor(lark.Visitor):
	def __init__(self,symtable,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.symtable=symtable
		self.ok=True
	def visit_top_down(self,tree):
		for subtree in tree.iter_subtrees_topdown():
			self._call_userfunc(subtree)
		return tree
	def declaracao_variaveis(self,tree):
		tipo=tree.children[0]
		ID=tree.children[1]
		if tree.children[2].type=="END_COMMAND":
			previous=self.symtable.add_variable(
				name=ID.value,
				_type=tipo.children[0].value,
				scope=Symtable.get_scope(tree),
				line=tree.meta.line
			)
			if previous:
				print("variavel ou funcao ja declarada",ID.value) #TODO BETER msg
				self.ok=False
		else:
			NotImplemented # vector declaration
	def declaracao_retorno(self,tree):
		NotImplemented #TODO check if this expression type matches parent type
		scope=Symtable.get_scope(tree)
	def declaracao_funcoes(self,tree):
		tipo=tree.children[0]
		ID=tree.children[1]
		parametros=tree.children[3]
		args=[]
		#-------------------------------------------------------------
		#add function to symtable
		previous=self.symtable.add_function(
			name=ID.value,
			_type=tipo.children[0].value,
			scope=Symtable.get_scope(tree.parent),
			line=tree.meta.line,
			args=args
		)
		if previous:
			print("funcao ja declarada ",ID.value)
			self.ok=False
		#-------------------------------------------------------------
		#get params and add them to symtable

		for param in parametros.find_data("param"):
			param_tipo=param.children[0]
			param_ID=param.children[1]
			
			if len(param.children)==2:
				param_name=param_ID.value
				param_scope=Symtable.get_scope(param)
				previous=self.symtable.add_variable(
					name=param_name,
					_type=param_tipo.children[0].value,
					scope=param_scope,
					line=param.meta.line
				)
			else:
				raise NotImplemented # vector declaration

			if previous:
				print("variavel ja declarada",param_ID.value) #TODO BETER msg
				self.ok=False
			args.append(self.symtable.get(param_scope,param_name))
		

	def variavel(self,tree):
		ID=tree.children[0]
		if not self.symtable.get(tree,ID.value):
			self.ok=False
			print("varivel não definida ",ID)

def shape_tree(subtree,parent=None):
	if not isinstance(subtree,lark.Tree):
		return
	subtree.parent=parent
	subtree.extra={}
	for children in subtree.children:
		shape_tree(children,subtree)

def sem(fname,tree,complete_tree,no_output,show):
	b=True
	shape_tree(tree)
	symtable=Symtable()
	visitor=Visitor(symtable)
	visitor.visit_top_down(tree)
	b&=visitor.ok
	print("-"*16,"SYMTABLE","-"*16)
	print(*(f"{k}->{repr(v)}" for k,v in symtable.table.items()),sep="\n")
	exit()
	# return b,ans,symtable