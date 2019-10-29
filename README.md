# OBC - Simple C Compiler
This project implements a compiler for a simplified version of C
using python and Lark parsing library

## What is the difference between this language and C?

* only has 2 data types, int and void
* does not support recursion
* does not support structs
* does not support pointers
* no preprocessor

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