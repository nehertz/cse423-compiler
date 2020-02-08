import ply.yacc as yacc
from ply_scanner import tokens

"""
[x] Identifiers
[/] Variables
[/] Functions
[x] Keywords
[/] Arithmetic expressions
[/] Assignment
[ ] Boolean expressions
[x] Goto statements
[x] If / Else control flow
[/] Unary operators
[x] Return statements
[x] Break statements
[x] While loops
"""

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf

#TODO: Preprocessing #include<> stuff
start = 'funcDecl'

def p_empty(p):
    'empty :'
    pass

def p_statement_list(p):
    '''
    statement_list : empty
                   | statement SEMI statement_list
                   | whileLoop statement_list
                   | if_stmt statement_list

    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = (p[1], p[2])
    elif (len(p) == 4):
        p[0] = (p[1], p[2], p[3])
    else: 
        pass

    return p
def p_statement(p):
    '''
    statement : return_stmt
            | var_decl
            | var_assign
            | goto_stmt
            | break_stmt
            | empty
    '''
    p[0] = p[1]
    return p

#TODO: Type cast in C
#TODO: sizeof(), Pointers, dereferencing 
#TODO: Structure ->, . operators to be added
def p_expr(p):
    '''
    expr : logical_expr
    '''
    p[0] = p[1]
    return p

def p_logical_expr(p):
    '''
    logical_expr : compOps
                | logical_expr LOR compOps
                | logical_expr LAND compOps
                | logical_expr OR compOps
                | logical_expr XOR compOps
                | logical_expr AND compOps
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])
    return p

def p_compOps(p):
    '''
    compOps : shift_expr
            | compOps EQ shift_expr 
            | compOps NE shift_expr
            | compOps LE shift_expr
            | compOps GE shift_expr
            | compOps LANGLE shift_expr
            | compOps RANGLE shift_expr 
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = (p[2], p[1], p[3])
    return p

def p_shift_expr(p):
    '''
    shift_expr : additive_expr
            | shift_expr LSHIFT additive_expr
            | shift_expr RSHIFT additive_expr
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = (p[2], p[1], p[3])
    return p
def p_additive_expr(p):
    '''
    additive_expr : additive_expr PLUS multiplicative_expr
         | additive_expr MINUS multiplicative_expr
         | multiplicative_expr

    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = (p[2], p[1], p[3])
    return p

def p_multiplicative_expr(p):
    '''
    multiplicative_expr : multiplicative_expr TIMES cast_expr
                    | multiplicative_expr DIVIDE cast_expr 
                    | multiplicative_expr MODULO cast_expr   
                    | operand
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = (p[2], p[1], p[3])
    else: 
        pass 
    return p
def p_cast_expr(p):
    '''
    cast_expr : unary_expr 
            | type_spec cast_expr 
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = (p[1], p[2])
    return p    

def p_unary_expr(p):
    '''
    unary_expr : postfix_expr
                | INCREMENT unary_expr
                | DECREMENT unary_expr
                | unary_expr cast_expr
                | SIZEOF LPAREN unary_expr RPAREN
                | SIZEOF LPAREN type_spec RPAREN
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = ('Prefix', p[1], p[2])
    else:
        p[0] = (p[1], p[3])
    return p

#TODO: Check the if conditions
def p_postfix_expr(p):
    '''
    postfix_expr : operand 
                | postfix_expr INCREMENT
                | postfix_expr DECREMENT
                | postfix_expr PERIOD ID 
                | postfix_expr ARROW ID
                | postfix_expr LBRACKET expr RBRACKET
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = ('Postfix', p[1], p[2])
    elif (len(p) == 5):
        p[0] = ('ArrayElement', p[1], p[3])
    else: 
        pass
    

#TODO: String
def p_operand(p):
    ''' 
    operand : ID
            | NUMCONST
    '''

    p[0] = p[1]
    return p
    
# TODO: Add RETURN func_call later
# TODO: Add other types


def p_return_stmt(p):
    '''
    return_stmt : RETURN expr
                | RETURN var_assign
    '''
    
    p[0] = (p[1], p[2])
    return p
    

def p_var_decl(p):
    '''
    var_decl : type_spec ID
             | type_spec var_assign 
    '''
    p[0] = ('ASSIGN', p[1], p[2])
    return p
    
# TODO: Finish char impl in scanner and add it here (| ID EQUALS CHAR SEMI)
# TODO: Add support for +=, -=, etc.
def p_var_assign(p):
    '''
    var_assign : ID EQUALS expr
               | ID EQUALS STRING
               | LPAREN var_assign RPAREN
               | ID TIMESEQUAL expr
               | ID DIVEQUAL expr 
               | ID MODEQUAL expr 
               | ID PLUSEQUAL expr 
               | ID MINUSEQUAL expr 
               | ID LSHIFTEQUAL expr 
               | ID RSHIFTEQUAL expr 
               | ID ANDEQUAL expr
               | ID OREQUAL expr 
               | ID XOREQUAL expr
    '''
    p[0] = (p[2], p[1], p[3])
    return p
   

def p_typeSpecList(p):
    '''
    type_spec_list : type_spec_list COMMA type_spec ID
                   | type_spec ID
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[3],p[2],p[1])
    return p


def p_typeSpec(p):
    '''
    type_spec : INT
                | CHAR
    '''
    p[0] = p[1]
    return p
# AUTO 
# | UNION 
# | SHORT 
# | DOUBLE 
# | LONG 
# | UNSIGNED 
# | INT 
# | CHAR 
# | STATIC 
# | VOLATILE 
# | STRUCT 
# | EXTERN 
# | SIGNED 
# | CONST 
# | ENUM 
# | VOID 
# | FLOAT

# def p_types(p):
#     '''
#     int : INT
#     char : CHAR
#     '''

def p_scope(p):
    '''
    scope : LBRACE statement_list RBRACE
    '''
    p[0] = ('LBRACE', p[2], 'RBRACE')
    return p

def p_args(p):
    '''
    args : type_spec_list
         | empty
    '''
    p[0] = p[1]
    return p

def p_funcDeclaration(p):
    '''
    funcDecl : type_spec ID LPAREN args RPAREN scope
    '''
    p[0] = ('Function', p[1], p[2], p[3], p[4], p[5], p[6])
    return p
    

def p_conditionals(p):
    '''
    conditionals    : expr
                    | TRUE
                    | FALSE
                    | LPAREN conditionals RPAREN
    '''
    
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = (p[1], p[2], p[3])
    return p
def p_whileLoop(p):
    '''
    whileLoop   : WHILE LPAREN conditionals RPAREN scope
    '''
    p[0] = ('WHILE', p[3], p[5])
    return p

def p_breakStmt(p):
    '''
    break_stmt  : BREAK
    '''
    p[0] = p[1]
    return p

def p_gotoStmt(p):
    '''
    goto_stmt  : GOTO ID 
    '''
    p[0] = ('GOTO', p[1], p[2])
    return p
    
def p_ifStmt(p):
    '''
    if_stmt : IF LPAREN conditionals RPAREN scope
            | IF LPAREN conditionals RPAREN scope elsiflist
    '''
    if (len(p) == 5):
        print("length 5")
        p[0] = ('IF', p[3], p[5])
    else: 
        print("length 6")
        p[0] = ('IF', p[3], p[5], p[6])
    return p
        
def p_elseIfList(p):
    '''
    elsiflist : ELSE IF LPAREN conditionals RPAREN scope elsiflist
            | ELSE IF LPAREN conditionals RPAREN scope
            | ELSE scope     
    '''
    if(len(p) == 3):
        p[0] = ('ElSE', p[2])
    elif (len(p) == 6):
        p[0] = ('ELSE IF', p[4], p[6])
    elif (len(p) == 7):
        p[0] = ('ELSE IF', p[4], p[6], p[7])
    return p
    
def p_error(t):
    print("Syntax error at {0}: Line Number: {1}".format(t.value, t.lineno))
    #print("Syntax error at '%s'" % t.value)

# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    result = parser.parse(lexer=lex)
    print(result)


    
