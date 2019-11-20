[![Build Status](https://travis-ci.com/llpinokio/obc.png?branch=master)](https://travis-ci.com/llpinokio/obc)
# OBC - Simple version of C NASM X86 linux Compiler
This project implements a compiler for a simplified version of C with error recovery
using python and Lark parsing library

## What is the difference between this language and C?
* only has 2 data types, int and void
* there is no preprocessor

### it does not support the following C features
* unary operators
* bitwise operators
* ternary operators
* structs
* pointers

for more information about it's syntax read [`src/grammar.lark`](src/grammar.lark)

### Builtin functions and variables
This language consists of the following builtin functions
|declaration|description|
|--|--|
|``` void putchar(int c)```|writes in the stdout the first byte indicated by the variable c.|
|``` void putstr(int str[])```|writes in the stdout all the first bytes indicated by the variable str, it must be null-ended.|
|``` void putint(int n)```|writes in the stdout a integer n.|
|``` int getchar(void)```|returns single byte read from stdin.|
|``` int getint(void)```|returns integer read from stdin.|
|```int SIZEOFINT```|represents the size in bytes of int variables (4)|


## Prerequisites

* python >= 3.6 (some source files have literal string interpolation)
* pip
* nasm

## Installing

Install all dependecies described in `requirements.txt` using pip

```bash
pip3 install -r requirements.txt
```
## Usage
cd to the src directory 

```bash
cd src
```

and call the compiler on some source file

```bash
./obc.py [SOURCE FILE PATH]
```

by default the following files representing the compiler's IO will be created:
* `tokens.dot,tokens.pdf`, representing the lexer output
* `syntax_tree.dot,syntax_tree.pdf`, representing the syntax analyzer output
* `symtable.dot,symtable.pdf,semantic_tree.dot,semantic_tree.pdf`, representing the semantic analyzer output
* `tac.txt`, representing the intermediate code generator output
* `code.nasm`, representing the code generator output
* `object.o`, representing the asembler output (NASM)
* `[program_name]`, representing the linker output (ld)

for more options use `/obc.py --help`