#!/usr/bin/env python3
import argparse
import os

parser=argparse.ArgumentParser()
parser.add_argument("input",type=argparse.FileType('r'),default="tokens.json",nargs='?')
# parser.add_argument("-o","--output",type=argparse.FileType('w'),default="") z
args=parser.parse_args()
print("-"*16,"ANALISADOR LÉXICO","-"*16)
os.system(f"./lex.py {args.input.name}")
print("-"*16,"ANALISADOR semantico","-"*16)
os.system(f"./syn.py tokens.json")
# os.system(f"./sem.py {args.input.name}")