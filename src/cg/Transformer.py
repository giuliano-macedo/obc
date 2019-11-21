import lark
def ignore():
	raise lark.Discard()
def flatten(l):
	# https://stackoverflow.com/a/12474246/5133524
	return sum(map(flatten,l),[]) if isinstance(l,list) else [l]
def tabify(l):
	for i,elem in enumerate(l):
		if isinstance(elem,str):
			l[i]="\t"+elem
		else:
			tabify(elem)
def common(s):
	if s.isnumeric():
		return s
	else:
		return f"[{s}]"
@lark.v_args(tree=True)
class Transformer(lark.Transformer):
	def __init__(self,symtable,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.symtable=symtable
	def tac(self,tree):
		return "\n".join(flatten(tree.children))
	def label(self,tree):
		tabify(tree.children)
		return [f"{tree.name}:"]+tree.children
	def attr(self,tree):
		if not tree.arg2.isnumeric():
			return [
				f"mov dword ebx,{common(tree.arg2)}",
				f"mov dword {common(tree.arg1)},ebx"
			]
		else:
			return [
				f"mov dword {common(tree.arg1)},{tree.arg2}"
			]
	def add(self,tree):
		return []
	def sub(self,tree):
		return []
	def mul(self,tree):
		return []
	def div(self,tree):
		return []
	def gt(self,tree):
		return []
	def gte(self,tree):
		return []
	def lt(self,tree):
		return []
	def lte(self,tree):
		return []
	def eq(self,tree):
		return []
	def neq(self,tree):
		return []
	def nop(self,tree):
		return []
	def ret(self,tree):
		return ["ret"]
	def arg(self,tree):
		#TODO IF VARIABLE IS VECTOR, DO NOT DEREFERENCIATE IT
		return [
			f"push dword {common(tree.arg1)}"
		]
	def call(self,tree):
		#TODO LOCAL VARIABLES BACKUP SOMEHOW
		return [
			f"call {tree.arg1}"
		]
	def ret_val(self,tree):
		return []
	def get_ret(self,tree):
		return []
	def set_vec(self,tree):
		return []
	def index(self,tree):
		if not tree.arg3.isnumeric():
			return [
				f"mov dword eax,{common(tree.arg3)}",
				f"mov dword ebx,[{tree.arg2}+eax*4]",
				f"mov dword [{tree.arg1}],ebx"
			]
		else:
			return [
				f"mov dword ebx,[{tree.arg2}+{int(tree.arg3)*4}]",
				f"mov dword [{tree.arg1}],ebx"
			]
	def set_at_index(self,tree):
		if tree.arg3.isnumeric() and tree.arg2.isnumeric():
			return [
				f"mov dword [{tree.arg1}+{int(tree.arg2)*4}],{tree.arg3}"
			]
		else:
			return[
				f"mov dword eax,{common(tree.arg2)}",
				f"mov dword ebx,{common(tree.arg3)}",
				f"mov dword [{tree.arg1}+eax*4],ebx"
			]
	def ifz_goto(self,tree):
		return []
	def ifnz_goto(self,tree):
		return []
	def got(self,tree):
		return []