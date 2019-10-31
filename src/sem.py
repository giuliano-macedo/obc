from collections import deque
import lark
class Symtable:
	class Entry:
		"""
		Symtable entry

		Attributes:
			type (str): variable or function type
			scope (str): name of parent function, "" if it's root of the code
			size (int): size of the vector, -1 if it's single variable
			referenced (bool): if the variable has changed
			initialized (bool): if the variable was initialized
			no_args (int): if variable this should be -1, if function, it must have the number of args
		"""
		def __init__(self,_type,scope,size,referenced,initialized,no_args):
			self.type=_type
			self.scope=scope
			self.size=size
			self.referenced=referenced
			self.initialized=initialized
			self.no_args=no_args
	class Visitor(lark.Visitor):
		def __init__(self,symtable,*args,**kwargs):
			super().__init__(*args,**kwargs)
			self.symtable=symtable
		def declaracao_variaveis(self,tree):
			tipo=tree.children[0]
			ID=tree.children[1]
			if tree.children[2].type=="END_COMMAND":
				added=self.symtable.add_variable(
					name=ID.value,
					_type=tipo.children[0],
					scope=Symtable.get_parent(tree)
				)
				if not added:
					print("variavel ja declarada",ID.value) #TODO BETER msg
			else:
				raise NotImplemented("vector declaration")
		def variavel(self,tree):

			ID=tree.children[0]
			if not self.symtable.get(tree,ID.value):
				print("varivel não definida ",ID)


	def __init__(self):
		self.table={}
	def add_variable(self,name,_type,scope):
		if self.table.get(scope+"."+name):
			return False
		self.table[scope+"."+name]=Symtable.Entry(
			_type=_type,
			scope=scope,
			size=-1,
			referenced=False,
			initialized=False,
			no_args=-1
		)
		print("variavel",name,"declarada no scopo",scope)
		return True
	def __getitem__(self,k):
		return self.table[k]
	def get(self,scope,k):
		return self.table.get((Symtable.get_parent(scope)+"."+k))
	def get_parent(tree):
		important=[]
		
		while tree:
			if tree.data=="declaracao_funcoes":
				important.append(tree.children[1].value)
			tree=tree.parent
		return ".".join(important[::-1])

	def build(self,tree):
		ans=True
		Symtable.Visitor(self).visit(tree)
		return ans
def add_parent_to_tree(subtree,parent=None):
	if not isinstance(subtree,lark.Tree):
		return
	subtree.parent=parent
	for children in subtree.children:
		add_parent_to_tree(children,subtree)

def sem(fname,tree,complete_tree,no_output,show):
	b=True
	add_parent_to_tree(tree)
	symtable=Symtable()
	b&=symtable.build(tree)

	exit()
	# return b,ans,symtable