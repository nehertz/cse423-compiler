import re
import ply.lex as lex

# use regex to remove comments at the beginning


keywords = ['else', 'register','do','goto','continue','if','sizeof','switch', 'for', 'case','while','break','default','return']
TypeSpecifier = ['int', 'auto', 'union', 'short', 'double','long', 'unsigned','int','char','static','volatile','struct','extern','signed','const','enum','void','float']

 # List of token names. Copy from TokenName.py 
tokens = ['TypeSpecifier','String','Identifier','NumberConstant',
        'SpecialCharacter', 'BitwiseOperator','ComparisonOperator',
        'Equals', 'Semicolon', 'LParen', 'RParen', 'LBracket',
        'RBracket', 'LCurly', 'RCurly', 'LAngle', 'RAngle',
        'ArithmeticOperator', 'Keyword', 'LogicalOperator',
        'AssignmentOperator','Comma', 'SingleQuot',
        'DoubleQuot', 'Increment', 'Decrement',
        'Colon'] + keywords + TypeSpecifier

#Ignor whitespace and tabs
t_ignore  = ' \t'

#Newline, keep track of line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    if (t.value in keywords):
        t.type = 'Keyword'
    elif (t.value in TypeSpecifier):
        t.type = 'TypeSpecifier'
    else:
        t.type = 'Identifier'
    return t

#String, got the regex from ply documentation 
def t_string(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.type = 'String'
    return t


#Number
def t_number(t):
    r'\d+'
    t.value = int(t.value)    
    t.type = 'NumberConstant'
    return t

#BitwiseOperator
def t_bitOps(t):
    r"(<<)|(>>)|(&)|(\|)|(\^)|(~)"
    t.type = 'BitwiseOperator'
    return t

#ComparisonOperator
def t_compOps(t):
    r"(==)|(\!=)|(>=)|(<=)"
    t.type = 'ComparisonOperator'
    return t

#AssignmentOperator
def t_assignOps(t):
    r"(=)|(\+=)|(-=)|(\*=)|(/=)|(%=)|(<<=)|(>>=)|(&=)|(\^=)|(\|=)"   
    t.type = 'AssignmentOperator'
    return t

#Increment
def t_increment(t):
    r'\+\+'
    t.type = 'Increment'
    return t

#Decrement
def t_decrement(t):
    r'\-\-'
    t.type = 'Decrement'
    return t

#ArithmeticOperator
def t_arithOps(t):
    r'[\/\+\-\*\%]'
    t.type = 'ArithmeticOperator'
    return t
#Comma
def t_comma(t):
    r'\,'
    t.type = 'Comma'
    return t

#SingleQuot
def t_singleQuot(t):
    r'\''  
    t.type = 'SingleQuot'
    return t

#DoubleQuot
def t_doubleQuot(t):
    r'\"'  
    t.type = 'DoubleQuot'
    return t

#Colon

#Equals

#LCurly

#RCurly

#LAngle

#RAngle 

#Left Bracket 
def t_lbracket(t):
    r'\{'
    t.type = 'LBracket'      
    return t

#Right Bracket 
def t_rbracket(t):
    r'\}'
    t.type = 'RBracket'      
    return t

#left paren
def t_lparan(t):
    r'\)'
    t.type = 'LParen'      
    return t

#right paren
def t_rparan(t):
    r'\('
    t.type = 'RParen'      
    return t

def t_simicolon(t):
    r'\;'
    t.type = 'Semicolon'      
    return t

#Error Handling 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def tokenizer(fileString):
    lexer = lex.lex()
    lexer.input(fileString)
    for tok in lexer:
        print("Toekn['" + str(tok.value)+ "' , '" + tok.type + "']")
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)
