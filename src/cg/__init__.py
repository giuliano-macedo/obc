import io
from .Transformer import Transformer
def cg(tac_tree,symtable):
	stdlib=open("cg/stdlib.asm").read()
	# scoped_symtable=scope_symtable(symtable)

	code=Transformer(symtable).transform(tac_tree)
	
	symtable_file=io.StringIO()
	for entry in symtable.table.values():
		if entry.is_function() or entry.is_builtin:continue
		name=f"{entry.scope}.{entry.name}"[1::]
		if not entry.is_vector():
			print(f"	{name.ljust(20)}:resb {'4'.ljust(10)};int",file=symtable_file)
		else:
			size=4 if entry.size==None else entry.size*4
			print(f"	{name.ljust(20)}:resb {str(size).ljust(10)};int[{'' if entry.size==None else entry.size}]",file=symtable_file)
	for i in range(tac_tree.max_level):
		name=f"t{i}"
		print(f"	{name.ljust(20)}:resb {'4'.ljust(10)};int",file=symtable_file)
	symtable_file.seek(0)

	open("code.asm","w").write(stdlib.format(code=code,symtable=symtable_file.read()))

	return True,