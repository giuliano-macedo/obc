from subprocess import check_output,CalledProcessError
import re
import os

def run(fname_path):
	return_code=0
	try:
		out=check_output(["python3","obc.py",fname_path])
	except CalledProcessError as e:
		return_code=e.returncode
		out=e.output
	if return_code!=0:
		return run_table.get(return_code,f"Unrecognized({return_code})")+"Error",out
	lines=out.decode("utf-8").split("\n")[::-1]
	last_aviso_index=next( (i  for i,line in enumerate(lines) if "[\x1b[35mAVISO\x1b[0m]" in line),None)
	if last_aviso_index==None:
		return "ok",out
	header=next( (line for line in lines[last_aviso_index:] if "-"*16 in line),None)
	if header==None:
		return "ok",out
	header_index=next((i for i,msg in enumerate(("ANALISADOR LÉXICO","ANALISADOR SINÁTICO","ANALISADOR SEMÂNTICO"),1) if msg in header),None)
	return run_table.get(header_index,f"Unrecognized")+"Warn",out

run_table={
	# 0:"ok",
	1:"Lexical",
	2:"Syntax",
	3:"Semantic"
}

extra_files={
	"TodosOsSimbolos":"SyntaxError",
	"mdc":"SemanticError",
	"emails":"LexicalError"
}
common={
	"lexical":{
		"err":"LexicalError",
		"warn":"LexicalWarn"
	},
	"syntax":{
		"err":"SyntaxError",
		"warn":"SyntaxWarn"
	},
	"semantic":{
		"err":"SemanticError",
		"warn":"SemanticWarn"
	}
}

fname_regex=re.compile(r"(lexical|syntax|semantic)_(warn|err).*")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

failed=False

for fname in sorted(os.listdir(os.path.join("..","samples"))):
	body,stem=os.path.splitext(fname)
	if stem != ".c":
		continue
	match=fname_regex.match(body)
	extra=extra_files.get(body)
	if match!=None:
		step=match.group(1)
		err_type=match.group(2)

		expected=common[step][err_type]
	elif extra!=None:
		expected=extra
	else:
		expected="ok"
	
	err,out=run(os.path.join("..","samples",fname))
	
	if err!=expected:
		print(f"error on file {repr(fname)}")
		print(f"it was expected {repr(expected)}, but got {repr(err)}")
		print("="*64)
		print(out.decode("utf-8"))
		failed=True
	else:
		print(f"{repr(fname)} OK")
print("="*64)
if failed:
	print("NOT OK")
	exit(-1)
else:
	print("OK")