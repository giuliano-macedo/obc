import lark
class TA(lark.Tree):
	table={
		"=": "attr",
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
		"nop":"nop",
		"ret":"ret",
		"arg":"arg",
		"call":"call",
		"rec":"rec",
		"ret_val":"ret_val",
		"get_ret":"get_ret",
		"set_vec":"set_vec"
	}
	def __init__(self,op,arg1=None,arg2=None,arg3=None):
		self.op=op
		self.arg1=str(arg1) if arg1 else arg1
		self.arg2=str(arg2) if arg2 else arg2
		self.arg3=str(arg3) if arg3 else arg3
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
		#fix this mess
		if self.op=="set_vec":
			return f"set_vec {self.arg1}={self.arg2}"
		n=self.no_args()
		if n==0:
			return self.op
		elif n==1:
			return f"{self.op} {self.arg1}"
		elif n==2:
			return f"{self.arg1}={self.arg2}"
		else:
			return "".join((str(self.arg1),"=",str(self.arg2),self.op,str(self.arg3) ))
	def __repr__(self):
		return f"TA{self.op,self.arg1,self.arg2,self.arg3}"

class Label(lark.Tree):
	def __init__(self,name,children):
		self.name=name
		super().__init__("label",children)
	def __repr__(self):
		return super().__repr__().replace("Tree","Label")