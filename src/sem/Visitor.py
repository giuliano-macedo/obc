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
		
		name=ID.value
		scope=Symtable.get_scope(tree)
		_type=tipo.children[0].value

		if _type!="int":
			self.onerr(
				tree.line,
				f"variável {repr(name)} definida como {repr(_type)} ela só pode ser de tipo 'int' ou 'vetor de int'"
			)

		if tree.children[2].type=="END_COMMAND": #regular variable
			previous=self.symtable.add_variable(
				name=name,
				_type=_type,
				scope=scope,
				line=tree.meta.line
			)
		else: #vector
			size=int(tree.children[3].value)
			if size==0:
				self.onerr(
					tree.line,
					f"vetor {repr(name)} não pode ser definido com tamanho 0"
				)
			previous=self.symtable.add_vector(
				name=name,
				_type=_type,
				scope=scope,
				line=tree.meta.line,
				size=size
			)
		if previous:
			self.onerr(
				tree.meta.line,
				Visitor.__var_already_declared(previous)
			)
			return
		tree.entry=self.symtable.get(scope,name)

	def declaracao_retorno(self,tree):
		
		scope=Symtable.get_scope(tree)
		is_return_void=(len(tree.children)==2)

		parent_function=tree
		while parent_function:
			if parent_function.data=="declaracao_funcoes":
				break
			parent_function=parent_function.parent
		if parent_function==None:
			self.onerr(
				tree.line,
				f"declaração de retorno em nenhuma função"
			)
		# 	return
		# if not(is_return_void and parent_function.entry.type=="void"):
		# 	self.onerr(
		# 		tree.line,
		# 		f"retorno de tipo {repr("int" if not is_return_void else "void")} numa função de tipo {repr(parent_function.entry.type)}"
		# 	)
		# 	return


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
		tree.entry=self.symtable.get(func_scope,func_name)
		if tree.entry.name=="main":
			tree.entry.referenced=True
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
			arg_var=self.symtable.get(param_scope,param_name)
			arg_var.referenced=True;
			arg_var.initialized=True;
			args.append(arg_var)
		
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
		tree.entry=var
		if not var.is_vector() and tree.expression.data=="vetor":
			self.onerr(
				tree.line,
				f"{repr(ID.value)} foi definida como varíavel na linha {var.line}, não vetor, impossível indexar"
			)
			return
		if tree.expression.data!="vetor":
			return
		exp=tree.expression.children[0]
		if isinstance(exp,int):
			if exp<0:
				self.onerr(
					tree.line,
					f"acesso negativo {repr(str(exp))} ao vetor {repr(ID.value)}"
				)
	def ativacao(self,tree):
		ID=tree.children[0]
		argumentos=tree.children[2]
		exp=tree.expression

		var=self.symtable.get(tree,ID.value)
		if not var:
			self.onerr(
				tree.line,
				f"função {repr(ID.value)} não declarada"
			)
			return
		tree.entry=var
		var.referenced=True

		are_args_vars=[not arg.is_vector() for arg in var.args]
		are_exps_vars=[]
		for e in exp.children:
			if isinstance(e,int): #if constant, True
				are_exps_vars.append(True)
			elif len(e.children)==0: #if is a single variable, and symtable returns vector, then it is false
				this_var=self.symtable.get(tree,e.var_name)
				if not this_var:
					return
				are_exps_vars.append(not this_var.is_vector())
			else: #there is complex expression, false expressions are ignored so this should as well
				are_exps_vars.append(True)
		
		if not (len(var.args)==len(exp.children) and all(x==y for x,y in zip(are_args_vars,are_exps_vars))):
			called_with=",".join(repr("int" if b else "vetor de int") for b in are_exps_vars)
			expected=",".join(repr("int" if b else "vetor de int") for b in are_args_vars)

			self.onerr(
				tree.line,
				f"função {repr(var.name)} definida na linha {var.line} foi chamada com variáveis {called_with} era esperado {expected}"
			)

