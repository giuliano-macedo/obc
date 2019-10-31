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
			return self.args!=None
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