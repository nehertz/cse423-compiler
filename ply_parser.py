import ply.yacc as yacc
from ply_scanner import tokens
from skbio import read
from skbio.tree import TreeNode
from syntaxTree import astConstruct

start = 'program'

def p_empty(p):
    'empty :'
    pass

# Start of the program
# Handles preprocessor, Global variable, and functions 
def p_program(p):
    '''
    program : declarationList
    '''
    return astConstruct(p, 'program')

def p_declarationList(p):
    '''
    declarationList : declarationList declaration 
                    | declaration
    '''
    return astConstruct(p, 'declarationList')

def p_declaration(p):
    '''
    declaration : PREPROC 
                | varDecl SEMI
                | enumDeclaration
    '''
    return astConstruct(p, 'declaration')

def p_enumInScope(p):
    '''
    enumInScope : ENUM ID ID SEMI
    '''
    return astConstruct(p, 'enumInScope')

def p_enumDeclaration(p):
    '''
    enumDeclaration :  funcList
                    | ENUM ID LBRACE enumArgs RBRACE SEMI
                    | ENUM LBRACE enumArgs RBRACE SEMI
                    | ENUM ID ID SEMI
    '''
    return astConstruct(p, 'enumDeclaration')

def p_enumArgs(p):
    '''
    enumArgs    : enumIDList
                | enumArgs COMMA enumIDList
    '''
    return astConstruct(p, 'enumArgs')

def p_enumIDList(p):
    '''
    enumIDList : ID 
                | ID EQUALS NUMCONST
    '''
    return astConstruct(p, 'enumIDList')


# Function Declaration  
def p_funcDeclaration(p):
    '''
    funcList : typeSpec ID LPAREN args RPAREN scope
    '''
    return astConstruct(p, 'funcList')

# TODO: Create operandList rule and add it here
def p_args(p):
    '''
    args : typeSpecList
         | operandList
         | empty
    '''
    return astConstruct(p, 'args')

def p_operandList(p):
    '''
    operandList : operandList COMMA operand
                | operand
    '''
    return astConstruct(p, 'operandList')

#TODO: String
def p_operand(p):
    ''' 
    operand : ID
            | NUMCONST
            | funcCall
            | LPAREN expr RPAREN
            | MINUS NUMCONST
            
    '''
    return astConstruct(p, 'operand')

# def p_idList(p):
#     '''
#     idList : idList COMMA ID
#            | ID
#     '''
#     return astConstruct(p, 'idList')

def p_scope(p):
    '''
    scope : LBRACE statementList RBRACE
    '''
    return astConstruct(p, 'scope')

def p_loopScope(p):
    '''
    loopScope : LBRACE loopStatementList RBRACE
    '''
    return astConstruct(p, 'loopScope')

def p_loopStatementList(p):
    '''
    loopStatementList    : breakStmt SEMI loopStatementList
                        | continueStmt SEMI loopStatementList
                        | statementList
    '''
    return astConstruct(p, 'loopStatementList')

def p_continueStmt(p):
    '''
    continueStmt    :  CONTINUE
    '''
    return astConstruct(p, 'continueStmt')
# variable Declaration 
def p_varDeclList(p):
    '''
    varDeclList : varDeclList varDecl SEMI
                | varDecl SEMI
    '''
    return astConstruct(p, 'varDeclList')

def p_varDecl(p):
    '''
    varDecl : combineTypeSpec
            | typeSpec ID
            | typeSpec varAssign
            | combineTypeSpec ID    
            | TYPEDEF typeSpec ID
            | TYPEDEF combineTypeSpec ID
            | EXTERN typeSpecPostfix ID
            | CONST EXTERN typeSpecPostfix ID
    '''
    return astConstruct(p, 'varDecl')



#TypeSpecifier Related Grammar 
def p_typeSpecList(p):
    '''
    typeSpecList : typeSpecList COMMA typeSpec ID
                 | typeSpec ID
    '''
    return astConstruct(p, 'typeSpecList')

### TOTAKECAREOF: register keyword can only be used within scope
### global variables are not allowed yet
### typedef not working yet
### Extern keyword can not have definition. That's why varDeclls
### has EXTERN 
def p_typeSpec(p):
    ''' 
    typeSpec : AUTO typeSpecPostfix
             | VOLATILE typeSpecPostfix
             | VOLATILE STATIC typeSpecPostfix
             | STATIC typeSpecPostfix
             | CONST typeSpecPostfix
             | REGISTER typeSpecPostfix
             | REGISTER STATIC typeSpecPostfix
             | typeSpecPostfix
             | combineType
    '''
    return astConstruct(p, 'typeSpec')

def p_combineTypeSpec(p):
    '''
    combineTypeSpec : combineType LBRACE varDeclList RBRACE
    '''
    return astConstruct(p, 'combineTypeSpec')

def p_combineType(p):
    '''
    combineType : STRUCT ID
                | UNION ID
    '''
    return astConstruct(p, 'combineType')

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
    return astConstruct(p, 'typeSpecPostfix')



# Statement Related Garmmars 
def p_statementList(p):
    '''
    statementList : empty
                  | statement SEMI statementList
                  | whileLoop statementList
                  | ifStmt statementList
                  | forLoop statementList
                  | switch statementList
                  | enumInScope statementList
    '''
    return astConstruct(p, 'statementList')

def p_statement(p):
    '''
    statement : returnStmt
              | varDecl
              | varAssign
              | gotoStmt
              | expr
              | empty
              | doWhile
    '''
    return astConstruct(p, 'statement')

# TODO: while loop scope supports break, continue, etc. 
# separate scope needs to be defined
def p_whileLoop(p):
    '''
    whileLoop : WHILE LPAREN conditionals RPAREN loopScope
    '''
    return astConstruct(p, 'whileLoop')

def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN conditionals RPAREN scope
           | IF LPAREN conditionals RPAREN scope elseIfList
    '''
    return astConstruct(p, 'ifStmt')
        
def p_elseIfList(p):
    '''
    elseIfList : ELSE IF LPAREN conditionals RPAREN scope elseIfList
               | ELSE IF LPAREN conditionals RPAREN scope
               | ELSE scope     
    '''
    return astConstruct(p, 'elseIfList')

def p_doWhile(p):
    '''
    doWhile : DO scope WHILE LPAREN conditionals RPAREN
    '''
    return astConstruct(p, 'doWhile')

def p_forLoop(p):
    '''
    forLoop : FOR LPAREN empty SEMI compOps SEMI empty RPAREN loopScope
            | FOR LPAREN init SEMI compOps SEMI empty RPAREN loopScope
            | FOR LPAREN empty SEMI compOps SEMI increase RPAREN loopScope
            | FOR LPAREN init SEMI compOps SEMI increase RPAREN loopScope
    '''
    return astConstruct(p, 'forLoop')

def p_forInit(p):
    '''
    init : typeSpec varAssign
         | varAssign
    '''
    return astConstruct(p, 'init')

def p_forIncrement(p):
    '''
    increase : varAssign
              | INCREMENT ID
              | DECREMENT ID
              | ID INCREMENT
              | ID DECREMENT 
    '''
    return astConstruct(p, 'increment')

def p_switch(p):
    '''
    switch : SWITCH LPAREN expr RPAREN switchscope 
    '''
    return astConstruct(p, 'switch')

def p_switchScope(p):
    '''
    switchscope : LBRACE caseList RBRACE
    '''
    return astConstruct(p, 'switchscope')

def p_caseList(p):
    '''
    caseList : CASE operand COLON statementList caseList
             | CASE CHARACTER COLON statementList caseList
             | CASE operand COLON statementList 
             | CASE CHARACTER COLON statementList 
             | DEFAULT COLON statementList
    '''
    return astConstruct(p, 'caseList')

# TODO: Add other types
def p_returnStmt(p):
    '''
    returnStmt : RETURN expr
               | RETURN varAssign
    '''
    return astConstruct(p, 'returnStmt')

def p_gotoStmt(p):
    '''
    gotoStmt : GOTO ID 
    '''
    return astConstruct(p, 'gotoStmt')

def p_breakStmt(p):
    '''
    breakStmt : BREAK
    '''
    return astConstruct(p, 'breakStmt')



def p_funcCall(p):
    '''
    funcCall : ID LPAREN args RPAREN
    '''
    return astConstruct(p, 'funcCall')



# Expression Related Grammars

#TODO: Type cast in C
#TODO: sizeof(), Pointers, dereferencing 
#TODO: Structure ->, . operators to be added
def p_expr(p):
    '''
    expr : logicalExpr
    '''
    return astConstruct(p, 'expr')

def p_logicalExpr(p):
    '''
    logicalExpr : compOps
                | logicalExpr LOR compOps
                | logicalExpr LAND compOps
                | logicalExpr OR compOps
                | logicalExpr XOR compOps
                | logicalExpr AND compOps
    '''
    return astConstruct(p, 'logicalExpr')

def p_compOps(p):
    '''
    compOps : shiftExpr
            | compOps EQ shiftExpr 
            | compOps NE shiftExpr
            | compOps LE shiftExpr
            | compOps GE shiftExpr
            | compOps LANGLE shiftExpr
            | compOps RANGLE shiftExpr 
    '''
    return astConstruct(p, 'compOps')

def p_shiftExpr(p):
    '''
    shiftExpr : additiveExpr
              | shiftExpr LSHIFT additiveExpr
              | shiftExpr RSHIFT additiveExpr
    '''
    return astConstruct(p, 'shiftExpr')

def p_additiveExpr(p):
    '''
    additiveExpr : additiveExpr PLUS multiplicativeExpr
                 | additiveExpr MINUS multiplicativeExpr
                 | multiplicativeExpr
    '''
    return astConstruct(p, 'additiveExpr')

def p_multiplicativeExpr(p):
    '''
    multiplicativeExpr : multiplicativeExpr TIMES castExpr
                       | multiplicativeExpr DIVIDE castExpr 
                       | multiplicativeExpr MODULO castExpr   
                       | castExpr
    '''
    return astConstruct(p, 'multiplicativeExpr')

def p_castExpr(p):
    '''
    castExpr : unaryExpr 
             | LPAREN typeSpec RPAREN castExpr 
    '''
    return astConstruct(p, 'castExpr') 

# Any unary operator and casting are not supported together.
def p_unaryExpr(p):
    '''
    unaryExpr : postfixExpr
              | LNOT unaryExpr
              | NOT unaryExpr
              | SIZEOF LPAREN unaryExpr RPAREN
              | SIZEOF LPAREN typeSpec RPAREN
              | unaryExpr INCREMENT
              | unaryExpr DECREMENT

    '''
    return astConstruct(p, 'unaryExpr') 

#TODO: Check the if conditions
# postfixExpr ARROW ID
def p_postfixExpr(p):
    '''
    postfixExpr : operand 
                | postfixExpr PERIOD ID
                | postfixExpr LBRACKET expr RBRACKET
                | INCREMENT postfixExpr
                | DECREMENT postfixExpr
    '''
    return astConstruct(p, 'postfixExpr') 

def p_varAssign(p):
    '''
    varAssign : ID EQUALS expr
              | ID EQUALS STRING
              | LPAREN varAssign RPAREN
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
    return astConstruct(p, 'varAssign') 

def p_conditionals(p):
    '''
    conditionals : expr
                 | TRUE
                 | FALSE
                 | LPAREN conditionals RPAREN
    '''
    return astConstruct(p, 'conditionals')

# Error Handling 
def p_error(t):
    print("Syntax error at {0}: Line Number: {1}".format(t.value, t.lineno))
   

# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    result = parser.parse(lexer=lex)
    s = '(' + str(result) + ')Program;'
    print(result)
    return s