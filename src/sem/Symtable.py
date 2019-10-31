from collections import deque
import lark
from .symtable_entries import VariableEntry,VectorEntry,FunctionEntry
class Symtable:
	def __init__(self):
		self.table={}
	def add_variable(self,name,_type,scope,line):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=VariableEntry(
			name=name,
			_type=_type,
			scope=scope,
			line=line
		)
	def add_function(self,name,_type,scope,line,args):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=FunctionEntry(
			name=name,
			_type=_type,
			scope=scope,
			line=line,
			arguments=args
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