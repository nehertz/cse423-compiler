import ply.yacc as yacc
from ply_scanner import tokens
from skbio import read
from skbio.tree import TreeNode
from syntaxTree import astConstrut

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
    return astConstrut(p, 'program')

def p_declarationList(p):
    '''
    declarationList : declarationList declaration 
                    | declaration
    '''
    return astConstrut(p, 'declarationList')

def p_declaration(p):
    '''
    declaration : PREPROC 
                | varDecl SEMI
                | funcList
    '''
    return astConstrut(p, 'declaration')



# Function Declaration  
def p_funcDeclaration(p):
    '''
    funcList : typeSpec ID LPAREN args RPAREN scope
    '''
    return astConstrut(p, 'funcList')

def p_args(p):
    '''
    args : typeSpecList
         | idList
         | empty
    '''
    return astConstrut(p, 'args')

def p_idList(p):
    '''
    idList : idList COMMA ID
           | ID
    '''
    return astConstrut(p, 'idList')

def p_scope(p):
    '''
    scope : LBRACE statementList RBRACE
    '''
    return astConstrut(p, 'scope')



# variable Declaration 
def p_varDeclList(p):
    '''
    varDeclList : varDeclList varDecl SEMI
                | varDecl SEMI
    '''
    return astConstrut(p, 'varDeclList')

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
    return astConstrut(p, 'varDecl')



#TypeSpecifier Related Grammar 
def p_typeSpecList(p):
    '''
    typeSpecList : typeSpecList COMMA typeSpec ID
                 | typeSpec ID
    '''
    return astConstrut(p, 'typeSpecList')

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
    return astConstrut(p, 'typeSpec')

def p_combineTypeSpec(p):
    '''
    combineTypeSpec : combineType LBRACE varDeclList RBRACE
    '''
    return astConstrut(p, 'combineTypeSpec')

def p_combineType(p):
    '''
    combineType : STRUCT ID
                | UNION ID
    '''
    return astConstrut(p, 'combineType')

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
    return astConstrut(p, 'typeSpecPostfix')



# Statement Related Garmmars 
def p_statementList(p):
    '''
    statementList : empty
                  | statement SEMI statementList
                  | whileLoop statementList
                  | ifStmt statementList
                  | doWhile statementList
                  | forLoop statementList
                  | switch statementList
    '''
    return astConstrut(p, 'statementList')

def p_statement(p):
    '''
    statement : returnStmt
              | varDecl
              | varAssign
              | gotoStmt
              | breakStmt
              | expr
              | funcCall
              | empty
    '''
    return astConstrut(p, 'statement')

def p_whileLoop(p):
    '''
    whileLoop : WHILE LPAREN conditionals RPAREN scope
    '''
    return astConstrut(p, 'whileLoop')

def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN conditionals RPAREN scope
           | IF LPAREN conditionals RPAREN scope elseIfList
    '''
    return astConstrut(p, 'ifStmt')
        
def p_elseIfList(p):
    '''
    elseIfList : ELSE IF LPAREN conditionals RPAREN scope elseIfList
               | ELSE IF LPAREN conditionals RPAREN scope
               | ELSE scope     
    '''
    return astConstrut(p, 'elseIfList')

def p_doWhile(p):
    '''
    doWhile : DO scope WHILE LPAREN conditionals RPAREN
    '''
    return astConstrut(p, 'doWhile')

def p_forLoop(p):
    '''
    forLoop : FOR LPAREN empty SEMI compOps SEMI empty RPAREN scope
            | FOR LPAREN init SEMI compOps SEMI empty RPAREN scope
            | FOR LPAREN empty SEMI compOps SEMI increment RPAREN scope
            | FOR LPAREN init SEMI compOps SEMI increment RPAREN scope
    '''
    return astConstrut(p, 'forLoop')

def p_forInit(p):
    '''
    init : typeSpec varAssign
         | varAssign
    '''
    return astConstrut(p, 'init')

def p_forIncrement(p):
    '''
    increment : varAssign
              | INCREMENT ID
              | DECREMENT ID
              | ID INCREMENT
              | ID DECREMENT 
    '''
    return astConstrut(p, 'increment')

def p_switch(p):
    '''
    switch : SWITCH LPAREN expr RPAREN switchscope 
    '''
    return astConstrut(p, 'switch')

def p_switchScope(p):
    '''
    switchscope : LBRACE caseList RBRACE
    '''
    return astConstrut(p, 'switchscope')

def p_caseList(p):
    '''
    caseList : CASE operand COLON statementList caseList
             | CASE CHARACTER COLON statementList caseList
             | CASE operand COLON statementList 
             | CASE CHARACTER COLON statementList 
             | DEFAULT COLON statementList
    '''
    return astConstrut(p, 'caseList')

# TODO: Add other types
def p_returnStmt(p):
    '''
    returnStmt : RETURN expr
               | RETURN varAssign
               | RETURN funcCall
    '''
    return astConstrut(p, 'returnStmt')

def p_gotoStmt(p):
    '''
    gotoStmt : GOTO ID 
    '''
    return astConstrut(p, 'gotoStmt')

def p_breakStmt(p):
    '''
    breakStmt : BREAK
    '''
    return astConstrut(p, 'breakStmt')

def p_funcCall(p):
    '''
    funcCall : ID LPAREN args RPAREN
    '''
    return astConstrut(p, 'funcCall')



# Expression Related Grammars

#TODO: Type cast in C
#TODO: sizeof(), Pointers, dereferencing 
#TODO: Structure ->, . operators to be added
def p_expr(p):
    '''
    expr : logicalExpr
    '''
    return astConstrut(p, 'expr')

def p_logicalExpr(p):
    '''
    logicalExpr : compOps
                | logicalExpr LOR compOps
                | logicalExpr LAND compOps
                | logicalExpr OR compOps
                | logicalExpr XOR compOps
                | logicalExpr AND compOps
    '''
    return astConstrut(p, 'logicalExpr')

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
    return astConstrut(p, 'compOps')

def p_shiftExpr(p):
    '''
    shiftExpr : additiveExpr
              | shiftExpr LSHIFT additiveExpr
              | shiftExpr RSHIFT additiveExpr
    '''
    return astConstrut(p, 'shiftExpr')

def p_additiveExpr(p):
    '''
    additiveExpr : additiveExpr PLUS multiplicativeExpr
                 | additiveExpr MINUS multiplicativeExpr
                 | multiplicativeExpr
    '''
    return astConstrut(p, 'additiveExpr')

def p_multiplicativeExpr(p):
    '''
    multiplicativeExpr : multiplicativeExpr TIMES castExpr
                       | multiplicativeExpr DIVIDE castExpr 
                       | multiplicativeExpr MODULO castExpr   
                       | operand
    '''
    return astConstrut(p, 'multiplicativeExpr')

def p_castExpr(p):
    '''
    castExpr : unaryExpr 
             | LPAREN typeSpec RPAREN castExpr 
    '''
    return astConstrut(p, 'castExpr') 

# Any unary operator and casting are not supported together.
def p_unaryExpr(p):
    '''
    unaryExpr : postfixExpr
              | INCREMENT unaryExpr
              | DECREMENT unaryExpr
              | SIZEOF LPAREN unaryExpr RPAREN
              | SIZEOF LPAREN typeSpec RPAREN
    '''
    return astConstrut(p, 'unaryExpr') 

#TODO: Check the if conditions
def p_postfixExpr(p):
    '''
    postfixExpr : operand 
                | postfixExpr INCREMENT
                | postfixExpr DECREMENT
                | postfixExpr PERIOD ID 
                | postfixExpr ARROW ID
                | postfixExpr LBRACKET expr RBRACKET
    '''
    return astConstrut(p, 'postfixExpr') 

#TODO: String
def p_operand(p):
    ''' 
    operand : ID
            | NUMCONST
    '''
    return astConstrut(p, 'operand') 

# TODO: Finish char impl in scanner and add it here (| ID EQUALS CHAR SEMI)
# TODO: Add support for +=, -=, etc.
def p_varAssign(p):
    '''
    varAssign : ID EQUALS expr
              | ID EQUALS STRING
              | ID EQUALS funcCall
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
    return astConstrut(p, 'varAssign') 

def p_conditionals(p):
    '''
    conditionals : expr
                 | TRUE
                 | FALSE
                 | LPAREN conditionals RPAREN
    '''
    return astConstrut(p, 'conditionals')

# Error Handling 
def p_error(t):
    print("Syntax error at {0}: Line Number: {1}".format(t.value, t.lineno))
   

# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    result = parser.parse(lexer=lex)
    print(result)
    s = '(' + str(result) + ')Program;'
    return s