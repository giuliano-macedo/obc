#!/usr/bin/env python3
import argparse
import os
from collections import namedtuple
import traceback
import sys

from lex import lex
from syn import syn
from sem import sem
from icg import icg
from cg import cg
class Hooks:
	Entry=namedtuple("HooksEntry",["func_name","func","kwargs"])
	def __init__(self):
		self.hooks={}
	def add_entry(self,func_prefix,func_name,func):
		self.hooks[func_prefix]=Hooks.Entry(func_name,func,{})
	def add_kwarg_to(self,func_prefix,k,v):
		self.hooks[func_prefix].kwargs[k]=v
	def items(self):
		"""

		Yields:
			tuple function_name,function"""
		for v in self.hooks.values():
			yield v.func_name,lambda *args:v.func(*args,**v.kwargs)

def command(cmd_str):
	print(cmd_str)
	try:
		os.system(cmd_str)
	except Exception as e:
		print(e)
		return False,
	return True,
parser=argparse.ArgumentParser()
parser.add_argument("input",type=argparse.FileType('r'))
parser.add_argument("-P","--pass-through",action="store_true",help="don't stop if some process returns error")
parser.add_argument("-N","--no-output",action="store_true",help="no output in every process")

parser.add_argument("--lex-no-output",action="store_true",help="no lex process output ('tokens.pdf','tokens.dot')")
parser.add_argument("--lex-show",action="store_true",help="no lex process tokens.pdf show")

parser.add_argument("-sC","--syn-complete-tree", action='store_true',help="render complete syntax tree, with full token leaves")
parser.add_argument("-sN","--syn-dont-try-to-fix-errs", action='store_true',help="disable parser ability to try to fix errors")
parser.add_argument("--syn-no-output",action="store_true",help="no syn process output ('syntax.pdf','syntax_tree.dot')")
parser.add_argument("--syn-show",action="store_true",help="no syn process syntax_tree.pdf show")

parser.add_argument("-SC","--sem-complete-tree", action='store_true',help="render complete semantic tree, with full token leaves")
parser.add_argument("--sem-no-output",action="store_true",help="no sem process output ('semantic_tree.pdf','semantic_tree.dot')")
parser.add_argument("--sem-show",action="store_true",help="no sem process semantic_tree.pdf show")

parser.add_argument("-IN","--icg-no-output",action="store_true",help="no icg process output (tac.txt)")

args=parser.parse_args()

if args.no_output:
	args.lex_no_output=True
	args.syn_no_output=True
	args.sem_no_output=True

hooks=Hooks()
hooks.add_entry("lex","ANALISADOR LÉXICO",lex)
hooks.add_entry("syn","ANALISADOR SINÁTICO",syn),
hooks.add_entry("sem","ANALISADOR SEMÂNTICO",sem)
hooks.add_entry("icg","GERADOR DE CÓDIGO INTERMEDIÁRIO",icg)
hooks.add_entry("cg","GERADOR DE CÓDIGO",cg)
hooks.add_entry("nasm","MONTADOR",lambda :command("nasm -felf32 code.asm -o object.o"))
fname_out=os.path.splitext(os.path.split(args.input.name)[-1])[0]
hooks.add_entry("ld","LINKADOR",lambda :command(f"ld -m elf_i386 object.o -o '{fname_out}'"))

for k,v in vars(args).items():
	k_splitted=k.split("_")
	if k_splitted[0] not in hooks.hooks:
		continue
	kwarg_key="_".join(k_splitted[1:])
	hooks.add_kwarg_to(k_splitted[0],kwarg_key,v)
ans=[args.input]
for i,(name,func) in enumerate(hooks.items(),1):
	print("-"*16,name,"-"*16)
	
	try:
		b,*ans=func(*ans)
	except Exception:
		exc_info = sys.exc_info()
		print("\x1b[1merro no compilador\x1b[0m")
		print("traceback:")
		traceback.print_exception(*exc_info)
		exit(i+80)
	if not b and not args.pass_through:
		exit(i)
exit(0)