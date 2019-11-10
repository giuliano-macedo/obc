import lark
from .horn import horn
from .TA import TA,Label
def ignore():
	raise lark.Discard()
@lark.v_args(tree=True)
class Transformer(lark.Transformer):
	def __init__(self,symtable,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.symtable=symtable
		self.max_level=0
	def programa(self,tree):
		ans=lark.Tree("tac",tree.children[0])
		ans.max_level=self.max_level
		return ans
	def lista_declaracoes(self,tree):
		if len(tree.children)==2:
			return tree.children[0]+tree.children[1]
		return tree.children[0]
	def declaracao(self,tree):
		return tree.children[0]
	def declaracao_variaveis(self,tree):
		ignore()
	def tipo(self,tree):
		ignore()
	def declaracao_funcoes(self,tree):
		var=tree.entry
		if var.type=="void":
			tree.children[-1].append(TA("ret"))
		return [Label(var.name,tree.children[-1])]
	def parametros(self,tree):
		ignore()
	def lista_parametros(self,tree):
		ignore()
	def param(self,tree):
		ignore()
	def declaracao_composta(self,tree):
		return tree.children[-2]
	def declaracao_locais(self,tree):
		ignore()
	def lista_comandos(self,tree):
		if len(tree.children)==2:
			return tree.children[0]+tree.children[1]
		return []
	def comando(self,tree):
		return tree.children[0]
	def declaracao_expressao(self,tree):
		if len(tree.children)==1:
			return [TA("nop")]
		return tree.children[0]
	def declaracao_selecao(self,tree):
		raise RuntimeError(NotImplemented)
	def declaracao_iteracao(self,tree):
		raise RuntimeError(NotImplemented)
	def declaracao_retorno(self,tree):
		if len(tree.children)==2:
			return [TA("ret")]
		l=tree.children[1]
		t=l[-1].arg1
		return l+[TA("ret_val",t),TA("ret")]

	def expressao(self,tree):
		if getattr(tree,"is_head",None)!=None:
			ans=horn(tree.expression)
			self.max_level=max(self.max_level,ans.level)
			return ans.list
		return tree
	# def variavel(self,tree):

	# def expressao_simples(self,tree):

	# def op_relacional(self,tree):

	# def soma_expressao(self,tree):

	# def soma(self,tree):

	# def termo(self,tree):

	# def mult(self,tree):

	# def fator(self,tree):

	# def ativacao(self,tree):

	# def argumentos(self,tree):

	# def lista_argumentos(self,tree):
