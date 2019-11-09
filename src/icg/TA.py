import lark
class TA(lark.Tree):
	table={
		"=": "set",
		"+": "add",
		"-": "sub",
		"*": "mul",
		"/": "div",
		">": "gt",
		">=":"gte",
		"<": "lt",
		"<=":"lte",
		"==":"eq",
		"!=":"neq",
		"nop":"nop"
	}
	def __init__(self,op,arg1=None,arg2=None,arg3=None):
		self.op=op
		self.arg1=arg1
		self.arg2=arg2
		self.arg3=arg3
		super().__init__(TA.table[op],[self.to_str()])
	def no_args(self):
		if self.arg1==None:
			return 0
		if self.arg2==None:
			return 1
		if self.arg3==None:
			return 2
		return 3
	def to_str(self):
		if self.no_args()==0:
			return self.op
		elif self.no_args()==2:
			return f"{self.arg1}={self.arg2}"
		else:
			return "".join((str(self.arg1),"=",str(self.arg2),self.op,str(self.arg3) ))
	def __repr__(self):
		return f"TA{self.op,self.arg1,self.arg2,self.arg3}"

class Label(lark.Tree):
	def __repr__(self):
		return super().__repr__().replace("Tree","Label")