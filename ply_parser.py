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
[ ] Goto statements
[ ] If / Else control flow
[ ] Unary operators
[x] Return statements
[ ] Break statements
[ ] While loops
"""
#TODO: Preprocessing #include<> stuff
start = 'funcDecl'

def p_empty(p):
    'empty :'
    pass

def p_statement_list(p):
    '''
    statement_list : empty
                   | statement SEMI statement_list
    statement : return_stmt
              | var_decl
              | var_assign
              | whileLoop
              | empty
    '''
def p_expr(p):
    '''
    expr : operand bin_op operand
    '''
def p_operand(p):
    '''
    operand : ID
            | NUMCONST
    '''
def p_bin_op(p):
    '''
    bin_op : PLUS
           | MINUS
           | TIMES
           | DIVIDE
           | MODULO
    '''
# TODO: Add RETURN func_call later
# TODO: Add other types
def p_return_stmt(p):
    '''
    return_stmt : RETURN operand
                | RETURN expr
                | RETURN var_assign
    '''

def p_var_decl(p):
    '''
    var_decl : type_spec ID
             | type_spec var_assign
    '''

# TODO: Finish char impl in scanner and add it here (| ID EQUALS CHAR SEMI)
# TODO: Add support for +=, -=, etc.
def p_var_assign(p):
    '''
    var_assign : ID EQUALS operand
               | ID EQUALS expr
               | ID EQUALS STRING
               | LPAREN var_assign RPAREN
    '''

def p_typeSpec(p):
    '''
    type_spec_list : type_spec_list COMMA type_spec ID
                   | type_spec ID
    type_spec : INT
              | CHAR
    '''

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

def p_funcDeclaration(p):
    '''
    funcDecl : type_spec ID LPAREN args RPAREN scope
    args : type_spec_list
         | empty
    '''
# def p_compOps(p):
#     '''
#     compOps     : LE
#                 | GE
#                 | EQ
#                 | NE
#     '''
# def p_conditionals(p):
#     '''
#     conditionals    : operand compOps operand
#                     | TRUE
#                     | FALSE
#                     | LPAREN conditionals RPAREN
#     '''
# def p_whileLoop(p):
#     '''
#     whileLoop   : WHILE LPAREN conditionals RPAREN scope
#     '''
def p_error(t):
    # print("Syntax error at '%s' line number: '%d'" % t.value, t.lineno)
    print("Syntax error at {0}: Line Number: {1}".format(t.value, t.lineno))

# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    result = parser.parse(lexer=lex)
    #print(result)
    
