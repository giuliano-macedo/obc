# OBC - Simple C Compiler
This project implements a compiler for a simplified version of C
using python and Lark parsing library

## What is the difference between this language and C?
* only has 2 data types, int and void (even though you can't declare negative numbers)
* there is no preprocessor

### it does not support the following features
* unary operators
* bitwise operators
* ternary operators
* structs
* pointers

for more information about it's syntax read `src/grammar.lark`
## Prerequisites

* python >= 3.6 (some source files have literal string interpolation)
* pip

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