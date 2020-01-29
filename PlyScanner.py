import re
import ply.lex as lex

keywords = {
    'int':'keyword',
    'return':'keyword'
}

 # List of token names. Copy from TokenName.py 
tokens = ['TypeSpecifier','String','Identifier','NumberConstant',
        'SpecialCharacter', 'BitwiseOperator','ComparisonOperator',
        'Equals', 'Semicolon', 'LParen', 'RParen', 'LBracket',
        'RBracket', 'LCurly', 'RCurly', 'LAngle', 'RAngle',
        'ArithmeticOperator', 'Keyword', 'LogicalOperator',
        'AssignmentOperator','Comma', 'SingleQuot',
        'DoubleQuot', 'Increment', 'Decrement',
        'Colon'] + list(keywords.values())

## WE can combine all following functions into one. 

# Identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = keywords.get(t.value,'Identifier')    
    return t

#Number
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    t.type = 'NumberConstant'
    return t

#Newline, track of line number
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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

#Ignor whitespace and tabs
t_ignore  = ' \t'

def tokenizer(fileString):
    lexer = lex.lex()
    lexer.input(fileString)
    for tok in lexer:
        print(tok)
        #print(tok.type, tok.value, tok.lineno, tok.lexpos)
