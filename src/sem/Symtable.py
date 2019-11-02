from collections import deque
import lark
from .symtable_entries import VariableEntry,VectorEntry,FunctionEntry
import graphviz
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
	def add_vector(self,name,_type,scope,line,size):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=VectorEntry(
			name=name,
			_type=_type,
			scope=scope,
			line=line,
			size=size
		)
	def __getitem__(self,k):
		return self.table[k]
	def get(self,scope,k):
		if isinstance(scope,lark.Tree):
			scope=Symtable.get_scope(scope)
		local=self.table.get((scope+"."+k))
		if local==None:
			return self.table.get("."+k) #try to return global
		return local
	def get_scope(tree):
		important=[]
		
		while tree:
			if tree.data=="declaracao_funcoes":
				important.append(tree.children[1].value)
			if tree.data=="programa":
				important.append("")
			tree=tree.parent
		return ".".join(important[::-1])
	def to_graphviz(self):
		ans=graphviz.Digraph(
			graph_attr={
				"rankdir":"LR",
				"nodesep":"0.5"
			},
			node_attr={
				"shape":"record",
				"width":".1",
				"height":".1"
			}
		)
		ans.node("ks",label="|".join(f"<k{i}> {k}" for i,k in enumerate(self.table.keys())))
		vs=[]
		for i,values in enumerate(self.table.values()):
			vs.append(
				f"{{<v{i}> "+	 
				"%s}"%"|".join(f"{k}={v}" for k,v in vars(values).items() if not isinstance(v,list))
			)
		ans.node("vs",label="|".join(vs))
		
		for i in range(len(self.table)):
			ans.edge(f"ks:k{i}",f"vs:v{i}")
		return ans