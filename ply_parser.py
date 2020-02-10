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


#TODO: Preprocessing #include<> stuff
start = 'program'

def p_empty(p):
    'empty :'
    pass

def p_statement_list(p):
    '''
    statement_list : empty
                   | statement SEMI statement_list
                   | whileLoop statement_list
                   | if_stmt statement_list
                   | dowhile statement_list
                   | forloop statement_list
                   | switch statement_list
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
              | expr
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
              | LPAREN type_spec RPAREN cast_expr 
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = (p[1], p[2])
    return p    
# Any unary operator and casting are not supported together.
def p_unary_expr(p):
    '''
    unary_expr : postfix_expr
               | INCREMENT unary_expr
               | DECREMENT unary_expr
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
             | combine_type ID
             | combine_type_spec
             | combine_type_spec ID
             | type_spec var_assign
             | TYPEDEF type_spec ID
             | TYPEDEF combine_type_spec ID
             | EXTERN typeSpecPostfix ID
             | CONST EXTERN typeSpecPostfix ID
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (p[1] == 'typedef'):
        p[0] = ('TYPEDEF', p[2], p[3])
    else:
        p[0] = ('ASSIGN', p[1], p[2])
    return p

def p_var_decl_list(p):
    '''
    var_decl_list : var_decl_list var_decl SEMI
                  | var_decl SEMI
    '''
    if (len(p) == 4):
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]
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

#TOTAKECAREOF: register keyword can only be used within scope
# global variables are not allowed yet
# typedef not working yet
# Extern keyword can not have definition. That's why var_decl
# has EXTERN 
def p_type_spec(p):
    ''' 
    type_spec : AUTO typeSpecPostfix
              | VOLATILE typeSpecPostfix
              | VOLATILE STATIC typeSpecPostfix
              | STATIC typeSpecPostfix
              | CONST typeSpecPostfix
              | REGISTER typeSpecPostfix
              | REGISTER STATIC typeSpecPostfix
              | typeSpecPostfix
              | combine_type
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3): 
        p[0] = (p[1], p[2])
    elif (len(p) == 4):
        p[0] = (p[1] + ' ' + p[2], p[3])
    return p

def p_combine_type_spec(p):
    '''
    combine_type_spec : combine_type LBRACE var_decl_list RBRACE
    '''
    if (len(p) == 5):
        p[0] = (p[1], p[2], p[3], p[4])
    else:
        p[0] = (p[1], p[5], p[2], p[3], p[4])
    return p

def p_combine_type(p):
    '''
    combine_type : STRUCT ID
                 | UNION ID
    '''
    p[0] = (p[1], p[2])
    return p

#TODO: union/struct, 
#Warning: float, double can't be signed/unsigned
def p_typeSpecPostfix(p):
    '''
    typeSpecPostfix : INT
                    | CHAR
                    | SHORT
                    | LONG
                    | FLOAT
                    | DOUBLE
                    | UNSIGNED INT
                    | SIGNED INT
                    | SHORT INT
                    | LONG INT
                    | LONG LONG INT
                    | UNSIGNED CHAR
                    | SIGNED CHAR 
                    | LONG LONG 
                    | SIGNED LONG 
                    | UNSIGNED LONG 
                    | LONG DOUBLE
                    | SIGNED SHORT
                    | UNSIGNED SHORT 
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3): 
        p[0] = (p[1], p[2])
    else: 
        p[0] = (p[1], p[2], p[3])
    return p

def p_gotoStmt(p):
    '''
    goto_stmt : GOTO ID 
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
    elif (len(p) == 7):
        p[0] = ('ELSE IF', p[4], p[6])
    elif (len(p) == 8):
        p[0] = ('ELSE IF', p[4], p[6], p[7])
    return p

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

def p_program(p):
    '''
    program : funclist
    '''
    p[0] = p[1]
    return p

def p_funcDeclaration(p):
    '''
    funclist : type_spec ID LPAREN args RPAREN scope funclist
            | type_spec ID LPAREN args RPAREN scope
    '''
    p[0] = ('Function', p[1], p[2], p[3], p[4], p[5], p[6])
    return p
  
def p_conditionals(p):
    '''
    conditionals : expr
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
    whileLoop : WHILE LPAREN conditionals RPAREN scope
    '''
    p[0] = ('WHILE', p[3], p[5])
    return p

def p_dowhile(p):
    '''
    dowhile : DO scope WHILE LPAREN conditionals RPAREN
    '''
    p[0] = ('DOWHILE', p[2], p[5])
    return p

def p_forInit(p):

    '''
    init : type_spec var_assign
        | var_assign
    '''
    if(len(p) == 3):
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]
    return p

def p_forIncrement(p):
    '''
    increment : var_assign
                | INCREMENT ID
                | DECREMENT ID
                | ID INCREMENT
                | ID DECREMENT 
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])
    return p


def p_forloop(p):
    '''
    forloop : FOR LPAREN empty SEMI compOps SEMI empty RPAREN scope
            | FOR LPAREN init SEMI compOps SEMI empty RPAREN scope
            | FOR LPAREN empty SEMI compOps SEMI increment RPAREN scope
            | FOR LPAREN init SEMI compOps SEMI increment RPAREN scope
    '''
    p[0] = ("FOR", p[3],p[5],p[7],p[9])
    return p

def p_breakStmt(p):
    '''
    break_stmt : BREAK
    '''
    p[0] = p[1]
    return p

def p_caseList(p):

    '''
    caselist : CASE operand COLON statement_list caselist
            | CASE operand COLON statement_list 
            | DEFAULT COLON statement_list
    '''
    if(len(p) == 6):
        p[0] = ('CASE', p[2], p[4], p[5])
    if(len(p) == 5):
        p[0] = ('CASE', p[2], p[4])
    if(len(p) == 4):
        p[0] = ('DEFAULT', p[3])
    return p
    
def p_switchScope(p):
    '''
    switchscope : LBRACE caselist RBRACE
    '''
    p[0] = p[2] 
    return p

def p_switch(p):

    '''
    switch : SWITCH LPAREN expr RPAREN switchscope 
    '''
    p[0] = ('SWITCH', p[3], p[5])
    return p

def p_error(t):
    print("Syntax error at {0}: Line Number: {1}".format(t.value, t.lineno))
    #print("Syntax error at '%s'" % t.value)

# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    result = parser.parse(lexer=lex)
    print(result)