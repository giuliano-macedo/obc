from collections import deque
import lark
from .symtable_entries import VariableEntry,VectorEntry,FunctionEntry
import graphviz
from . import myrepr
class Symtable:
	def __init__(self):
		self.table={}
		#std 'prototypes'

		#input
		#------------------------------------------------------------------------
		# int getchar(void)
		self.add_function("getchar","int","",0,[],does_return=True,referenced=True,is_builtin=True)
		# int getint(void)
		self.add_function("getint","int","",0,[],does_return=True,referenced=True,is_builtin=True)
		#output
		#------------------------------------------------------------------------
		# void putint(int n)
		args=[]
		self.add_function("putint","void","",0,args,does_return=True,referenced=True,is_builtin=True)
		self.add_variable("n","int","putint",0,initialized=True,referenced=True,is_builtin=True)
		args.append(self.get("putint","n"))

		# void putstr(int str[]) ; must be null ended
		args=[]
		self.add_function("putstr","void","",0,args,does_return=True,referenced=True,is_builtin=True)
		self.add_vector("str","int","putstr",0,None,initialized=True,referenced=True,is_builtin=True)
		args.append(self.get("putstr","str"))

		
		# void putchar(int c);
		args=[]
		self.add_function("putchar","void","",0,args,does_return=True,referenced=True,is_builtin=True)
		self.add_variable("c","int","putchar",0,initialized=True,referenced=True,is_builtin=True)
		args.append(self.get("putchar","c"))

		#'contants'
		#------------------------------------------------------------
		
		self.add_variable("SIZEOFINT","int","",0,initialized=True,referenced=True,is_builtin=True)# int SIZEOFINT=4;

	def add_variable(self,name,_type,scope,line,**kwargs):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=VariableEntry(
			name=name,
			_type=_type,
			scope=scope,
			line=line,
			**kwargs
		)
	def add_function(self,name,_type,scope,line,args,**kwargs):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=FunctionEntry(
			name=name,
			_type=_type,
			scope=scope,
			line=line,
			arguments=args,
			**kwargs
		)
	def add_vector(self,name,_type,scope,line,size,**kwargs):
		var=self.table.get(scope+"."+name,None)
		if var!=None:
			return var
		self.table[scope+"."+name]=VectorEntry(
			name=name,
			_type=_type,
			scope=scope,
			line=line,
			size=size,
			**kwargs
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
			row="|".join(f"{k}={myrepr(v)}" for k,v in vars(values).items())
			if values.is_function():
				row="Function|"+row
			elif not values.is_vector():
				row="Variable|"+row
			else:
				row="Vector|"+row
			vs.append(f"{{<v{i}> {row}}}")
		ans.node("vs",label="|".join(vs))
		
		for i in range(len(self.table)):
			ans.edge(f"ks:k{i}",f"vs:v{i}")
		return ans