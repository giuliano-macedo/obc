from .Transformer import Transformer
def icg(tree,symtable):
	b=True
	tac_tree=Transformer(symtable).transform(tree)


	print(tac_tree.pretty())
	print(tac_tree)
	print("max level:",tac_tree.max_level)
	exit()
	# return b