import lark
from .Symtable import Symtable
class Visitor(lark.Visitor):
	def __init__(self,symtable,onerr,onwarn,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.symtable=symtable
		self.onerr=onerr
		self.onwarn=onwarn
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
				self.onerr(
					tree.meta.line,
					Visitor.__var_already_declared(previous)
				)
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
			self.onerr(
				tree.meta.line,
				Visitor.__var_already_declared(previous)
			)
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
				self.onerr(
					param.meta.line,
					Visitor.__var_already_declared(previous)
				)
				self.ok=False
			args.append(self.symtable.get(param_scope,param_name))
		
	def __var_already_declared(previous):
		f_or_var='variavel' if previous.is_var() else 'função'
		return f"{f_or_var} {repr(previous.name)} ja foi declarada como {repr(previous.type)} na linha {previous.line}"
	def variavel(self,tree):
		ID=tree.children[0]
		if not self.symtable.get(tree,ID.value):
			self.onerr(
				tree.line,
				f"variavel {repr(ID.value)} não declarada"
			)
			self.ok=False
