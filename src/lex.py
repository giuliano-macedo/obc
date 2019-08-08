#!/usr/bin/env python3
import ox
import argparse
def lex(f):
	st=lambda s:(s.upper(),s) #SIMPLE_TOKEN
	lexer = ox.make_lexer([
		st("if"),
		st("else"),
		st("int"),
		st("void"),
		st("return"),
		st("while"),
		("ARIOP",r"\+|\-|\*|\/"),
		("RELOP",r"<|<=|>|>=|==|\!="),
		("ATTR",r"="),
		("END_COMMAND",r"\;"),
		("COMMA",r"\,"),
		
		("P_OPEN",r"\("),
		("P_CLOSE",r"\)"),

		("S_OPEN",r"\["),
		("S_CLOSE",r"\]"),

		("B_OPEN",r"\{"),
		("B_CLOSE",r"\}"),

		("COMMENT_START",r"\/\*"),
		("COMMENT_STOP",r"\*\/"),

		("ID",r"[a-zA-Z]+"),
		("NUM",r"[0-9]+"),
	])
	return lexer(f.read())
if __name__=="__main__":
	parser=argparse.ArgumentParser()
	parser.add_argument("input",type=argparse.FileType('r'))
	args=parser.parse_args()

	print(lex(args.input))
	