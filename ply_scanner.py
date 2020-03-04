import re
import ply.lex as lex

keywords = ['else', 'register','do','goto','continue','if','sizeof','switch', 'for', 'case','while','break','default','return', 'typedef', 'define', 'include']
type_specifier = ['auto', 'union', 'short', 'double','long', 'unsigned','int','char','static','volatile','struct','extern','signed','const','enum','void','float']
assignment = ['=' ,'*=', '/=', '%=', '+=', '-=']

operators = {
    # Logical operators
    '||' : 'LOR',
    '&&' : 'LAND',

    # Bitwise operators
    '<<=' : 'LSHIFTEQUAL',
    '>>=' : 'RSHIFTEQUAL',

    '<<' : 'LSHIFT',
    '>>' : 'RSHIFT',
    
    # Comparison operators
    # '<' : 'LT',
    # '>' : 'GT',
    '<=' : 'LE',
    '>=' : 'GE',
    '==' : 'EQ',
    '!=' : 'NE',
    '!' : 'LNOT',


    # Assignment operators
    '=' : 'EQUALS',
    '*=' : 'TIMESEQUAL',
    '/=' : 'DIVEQUAL',
    '%=' : 'MODEQUAL',
    '+=' : 'PLUSEQUAL',
    '-=' : 'MINUSEQUAL',
   
   
    '&=' : 'ANDEQUAL',
    '|=' : 'OREQUAL',
    '^=' : 'XOREQUAL',

    # Increment/decrement
    '++' : 'INCREMENT',
    '--' : 'DECREMENT',

    # ->
    '->' : 'ARROW',

    # Delimiters
    '(' : 'LPAREN',
    ')' : 'RPAREN',
    '[' : 'LBRACKET',
    ']' : 'RBRACKET',
    '{' : 'LBRACE',
    '}' : 'RBRACE',
    ',' : 'COMMA',
    '.' : 'PERIOD',
    ';' : 'SEMI',
    ':' : 'COLON',
    '\'' : 'SQUOT',
    '\"' : 'DQUOT',
    '<' : 'LANGLE',
    '>' : 'RANGLE',
    '...' : 'ELLIPSIS',

    # Arithmetic operators 
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'TIMES',
    '/' : 'DIVIDE',
    '%' : 'MODULO',

    # Boolean
    'TRUE' : 'TRUE',
    'FALSE' : 'FALSE',

    '|' : 'OR',
    '&' : 'AND',
    '~' : 'NOT',
    '^' : 'XOR',
}

tokens = ['STRING','CHARACTER','ID', 'NUMCONST', 'PREPROC'] + [keyword.upper() for keyword in keywords] + [t.upper() for t in type_specifier] + list(operators.values())

# Ignore whitespace and tabs
t_ignore  = ' \t'

# Newline, keep track of line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Skip Line Comments
def t_comments(t):
    r'\/\/(.)*'
    pass

# Skip Block comments
def t_blockComments(t):
    r'(\/\*)[\s\S]*(\*\/)'
    # TODO: newlines inside of block comments will mess with following line numbers
    pass

# Preprocessors
def t_preproc(t):
    r'\#include<[a-zA-Z]+\.\w>|\#include\"[a-zA-Z]+\.\w\"'
    t.type = 'PREPROC'
    return t

# Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    if (t.value in keywords):
        t.type = t.value.upper()
    elif (t.value in type_specifier):
        t.type = t.value.upper()
    elif (t.value == "TRUE"):
        t.type = t.value.upper()
    elif (t.value == "FALSE"):
        t.type = t.value.upper()
    else:
        t.type = 'ID'
    return t

# String, got the regex from ply documentation 
def t_string(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.type = 'STRING'
    return t

# Single Character
def t_character(t):
    r'\'.\''
    t.type = 'CHARACTER'
    return t

# binary number 
def t_binary(t):
    r'0b[01]+'
    t.value = int(t.value,2)
    t.type = 'NUMCONST'
    return t

# Hex number Stolen from Stackoverflow but modified to accpect both 0X and 0x 
def t_hex(t):
    r'0[xX]([abcdef]|\d)+'
    t.value = int(t.value, 16)
    t.type = 'NUMCONST'
    return t

# Floating Point Number
def t_float(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    t.type = 'NUMCONST'
    return t

# Integer Number
def t_number(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'NUMCONST'
    return t

# ComparisonOperator
def t_compOps(t):
    r"(==)|(\!=)|(>=)|(<=)"
    t.type = operators.get(t.value)
    return t

# AssignmentOperator
def t_assignOps(t):
    r"(=)|(\+=)|(-=)|(\*=)|(/=)|(%=)|(<<=)|(>>=)|(&=)|(\^=)|(\|=)"   
    t.type = operators.get(t.value)
    return t
    
# Logic Operator
def t_logicOps(t):
    r"(\|\|)|(&&)|(\!)"
    t.type = operators.get(t.value)
    return t

# BitwiseOperator
def t_bitOps(t):
    r"(<<)|(>>)|(&)|(\|)|(\^)|(~)"
    t.type = operators.get(t.value)
    return t

# Increment and Decrement 
def t_increment(t):
    r'\-\-|\+\+'
    t.type = operators.get(t.value)
    return t

# ArithmeticOperator
def t_arithOps(t):
    r'[\/\+\-\*\%]'
    t.type = operators.get(t.value)
    return t

# Delimiters
def t_delimiters(t):
    r'\,|\'|\"|\:|\{|\}|\<|\>|\[|\]|\(|\)|\;|\.'
    t.type = operators.get(t.value)
    return t

# Error Handling 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer and input the file string into lexer
# parameters: fileString, string of C source file 
def tokenizer(fileString):
    lexer = lex.lex()
    lexer.input(fileString)
    return lexer
