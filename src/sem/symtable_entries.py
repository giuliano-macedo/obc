class BaseEntry:
	def __init__(self,name,_type,scope,line,**kwargs):
		self.name=name
		self.type=_type
		self.scope=scope
		self.line=line
		self.referenced=kwargs.get("referenced",False)
		self.is_builtin=kwargs.get("is_builtin",False)
	def is_function(self): #virtual
		raise NotImplementedError()
	def is_var(self): #virtual
		raise NotImplementedError()
	def is_vector(self): #virtual
		raise NotImplementedError()
	def __str__(self):
		return repr(self)
	def __repr__(self):
		kwargs=",".join(f"{k}={repr(v)}" for k,v in vars(self).items())
		return f"Entry({kwargs})"
class VariableEntry(BaseEntry):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.initialized=kwargs.get("initialized",False)
	def is_function(self):
		return False
	def is_var(self):
		return True
	def is_vector(self):
		return False
	def __repr__(self):
		return super().__repr__().replace("Entry","VariableEntry")
class VectorEntry(VariableEntry):
	def __init__(self,*args,size,**kwargs):
		super().__init__(*args,**kwargs)
		self.size=size
	def is_function(self):
		return False
	def is_var(self):
		return True
	def is_vector(self):
		return True
	def __repr__(self):
		return super().__repr__().replace("VariableEntry","VectorEntry")
class FunctionEntry(BaseEntry):
	def __init__(self,*args,arguments,**kwargs):
		super().__init__(*args,**kwargs)
		self.args=arguments
		self.does_return=kwargs.get("does_return",False)
		self.no_ifs=0
		self.no_whiles=0
	def is_function(self):
		return True
	def is_var(self):
		return False
	def is_vector(self):
		return False
	def __repr__(self):
		return super().__repr__().replace("Entry","FunctionEntry")