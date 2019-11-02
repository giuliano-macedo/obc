import lark
from .Symtable import Symtable
class Visitor(lark.Visitor):
	
	def __init__(self,symtable,onerr,onwarn,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.symtable=symtable
		self.__onerr=onerr
		self.onwarn=onwarn
		self.ok=True
	def onerr(self,line,msg):
		self.__onerr(line,msg)
		self.ok=False
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
		else:
			size=int(tree.children[3].value)
			previous=self.symtable.add_vector(
				name=ID.value,
				_type=tipo.children[0].value,
				scope=Symtable.get_scope(tree),
				line=tree.meta.line,
				size=size
			)
		if previous:
			self.onerr(
				tree.meta.line,
				Visitor.__var_already_declared(previous)
			)

	def declaracao_retorno(self,tree):
		NotImplemented #TODO check if this expression type matches parent type
		scope=Symtable.get_scope(tree)
	def declaracao_funcoes(self,tree):
		tipo=tree.children[0]
		ID=tree.children[1]
		parametros=tree.children[3]
		args=[]
		func_scope=Symtable.get_scope(tree.parent)
		func_name=ID.value
		#-------------------------------------------------------------
		#add function to symtable
		previous=self.symtable.add_function(
			name=func_name,
			_type=tipo.children[0].value,
			scope=func_scope,
			line=tree.meta.line,
			args=args
		)
		if previous:
			self.onerr(
				tree.meta.line,
				Visitor.__var_already_declared(previous)
			)
			return
		func=self.symtable.get(func_scope,func_name)
		if func.name=="main":
			func.referenced=True
		#-------------------------------------------------------------
		#get params and add them to symtable

		for param in parametros.find_data("param"):
			param_tipo=param.children[0]
			param_ID=param.children[1]
			
			param_name=param_ID.value
			param_scope=Symtable.get_scope(param)
			if len(param.children)==2:
				previous=self.symtable.add_variable(
					name=param_name,
					_type=param_tipo.children[0].value,
					scope=param_scope,
					line=param.meta.line
				)
			else:
				previous=self.symtable.add_vector(
					name=param_name,
					_type=param_tipo.children[0].value,
					scope=param_scope,
					line=param.meta.line,
					size=None
				)

			if previous:
				self.onerr(
					param.meta.line,
					Visitor.__var_already_declared(previous)
				)
			args.append(self.symtable.get(param_scope,param_name))
		
	def __var_already_declared(previous):
		f_or_var='variável' if previous.is_var() else 'função'
		return f"{f_or_var} {repr(previous.name)} ja foi declarada como {repr(previous.type)} na linha {previous.line}"
	def variavel(self,tree):
		ID=tree.children[0]
		var=self.symtable.get(tree,ID.value)
		if not var:
			self.onerr(
				tree.line,
				f"variável {repr(ID.value)} não declarada"
			)
			return
		var.referenced=True
		exp_value=tree.expression.children[0]
		if var.is_vector and isinstance(exp_value,int):
			if exp_value<0:
				self.onerr(
					tree.line,
					f"acesso negativo {repr(str(exp_value))} ao vetor {repr(ID.value)}"
				)
