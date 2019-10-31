from lex import TOKENS_DEFINITION
from lark import Lark
from lark.lexer import Lexer, Token
from lark.exceptions import UnexpectedToken
from lark.grammar import Terminal
from graphviz import Digraph
from utils import log_err,log_war

TOKENS_NAMES=[t[0] for t in TOKENS_DEFINITION]

class Lex(Lexer):
	def __init__(self, lexer_conf):
		pass
	def lex(self, tokens):
		for token in tokens:
				yield token
def build_dot(tree,dot,complete=False):
	istoken=lambda obj:type(obj)==Token
	if complete:
		getData=lambda obj:rf"\<{obj.type},{obj.value}\>" if istoken(obj) else obj.data
	else :
		getData=lambda obj:obj if istoken(obj) else obj.data
	h=str(id(tree))
	label=getData(tree) if istoken(tree) else f"<<font face=\"boldfontname\">{getData(tree)}</font>>"
	dot.node(h,label=label)
	if istoken(tree):
		return 
	for children in tree.children:
		dot.edge(h,str(id(children)))
		build_dot(children,dot,complete)
with open("grammar.lark") as f:
	grammar=f.read() + f"\n%declare {' '.join(TOKENS_NAMES)}"

def informe_syntax_err(err,line_str):
	log_err(f"na linha {repr(line_str)}")
	print("\t"+f"número da linha:{err.line} coluna:{err.column}")
	print("\t"+f"era esperado um dos seguintes tokens {err.expected}")

def try_parse(parser,tokens):
	"""
	try parse using lark parser
	Returns:
		tuple (did_parsed,tree/err)
	"""
	try:
		tree = parser.parse(tokens)
	except UnexpectedToken as e:
		return (False,e)
	return (True,tree)
put_token_dict={k:v.replace("\\","") for k,v in TOKENS_DEFINITION if k not in {"ID","NUM"}}
def put_token(tokens,i,to_add_name):
	global put_token_dict 
	last_token=tokens[i]
	last_token_len=len(last_token.value)
	value=put_token_dict.get(to_add_name)
	if value==None:
		return -1
	tokens.insert(i,Token(
		to_add_name,
		value,
		line=last_token.line,
		column=last_token.column+last_token_len,
		pos_in_stream=last_token.pos_in_stream+last_token_len	
	))
	return i
def get_line_from_tokens(tokens,line):
	return " ".join((token.value for token in tokens if token.line==line))
def inform_line_changed(tokens,code_splitted,line):
	old_line=code_splitted[line-1].strip()
	new_line=get_line_from_tokens(tokens,line)
	log_war(f"linha '{old_line}' considerada como '{new_line}', número da linha :{line}")
def remove_line(tokens,line):
	for i in range(len(tokens)-1,-1,-1):
		if tokens[i].line ==line:
			# print("removing ",tokens[i])
			tokens.pop(i)

def syn(fname,tokens,complete_tree,dont_try_to_fix_errs,no_output,show):
	def try_to_put_expected_token(tokens): #TODO GLOBALS
		sucess=False
		expecteds=[expected for expected in e.expected if expected not in {"ID","NUM","SUMOP","RELOP","ARIOP","MULTOP","$END"}]
		expecteds.sort() #replicability
		if "COMMA" in expecteds: #PREFERENCE TO COMMA
			expecteds.insert(0,expecteds.pop(expecteds.index("COMMA")))
		for expected in expecteds:
			# print(f"trying to put {expected}")
			index_added=put_token(modified_tokens,token_index,expected)
			if index_added==-1:
				continue
			stop,e2=try_parse(lark,modified_tokens)
			if stop or not (e.line<=e2.line<=(e.line+1)):
				tokens=modified_tokens
				inform_line_changed(tokens,code_splitted,e.line)
				sucess=True
				break
			#removed last added token
			modified_tokens.pop(index_added)
		return sucess,tokens

	lark = Lark(grammar,parser='lalr',lexer=Lex,start="programa",propagate_positions=True)
	if len(tokens)==0:
		log_err("programa vazio")
		exit(-1)
	code=open(fname).read()
	code_splitted=code.split("\n")
	b=True
	while True:
		if len(tokens)==0:
			break
		did_parse,e=try_parse(lark,tokens)
		if did_parse:
			tree=e
			break
		modified_tokens=tokens.copy()
		token_index=next(i for i,token in enumerate(tokens) if token.line==e.line and token.column==e.column)
		#----------------try to put expected token----------------
		if not dont_try_to_fix_errs:
			worked,tokens=try_to_put_expected_token(tokens)
			if worked:
				continue
		#----------------remove whole line----------------
		remove_line(tokens,e.line)
		informe_syntax_err(e,code_splitted[e.line-1].strip())
		b=False

	if not no_output:
		dot = Digraph()
		if complete_tree:
			dot.attr(rankdir="LR")
		build_dot(tree,dot,complete=complete_tree)
		dot.save("syntax_tree.dot")
		dot.render('syntax_tree',format="pdf", cleanup=True,view=show,quiet_view=show)
	return b,fname,tree