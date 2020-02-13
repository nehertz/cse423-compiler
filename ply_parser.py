import ply.yacc as yacc
from ply_scanner import tokens
from skbio import read
from skbio.tree import TreeNode

#TODO: Preprocessing #include<> stuff
start = 'program'

def p_empty(p):
    'empty :'
    pass

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
    if(len(p) == 4 and p[3] != None):
        p[0] = '(' + str(p[1]) + ')' + ',' + str(p[3]) 
    elif(len(p) == 3 and p[2] != None):
        p[0] = '(' + str(p[1]) + ')'  + ',' + str(p[2])
    else:
        p[0] = p[1]
    
    return p

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
    
    p[0] = p[1]
    return p

def p_funcCall(p):
    '''
    funcCall : ID LPAREN args RPAREN
    '''

    p[0] = str(p[1]) + '(' + str(p[3]) + ')'
    return p

#TODO: Type cast in C
#TODO: sizeof(), Pointers, dereferencing 
#TODO: Structure ->, . operators to be added
def p_expr(p):
    '''
    expr : logicalExpr
    '''
    p[0] = p[1]
    return p

def p_logicalExpr(p):
    '''
    logicalExpr : compOps
                | logicalExpr LOR compOps
                | logicalExpr LAND compOps
                | logicalExpr OR compOps
                | logicalExpr XOR compOps
                | logicalExpr AND compOps
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
    return p

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
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
    return p

def p_shiftExpr(p):
    '''
    shiftExpr : additiveExpr
              | shiftExpr LSHIFT additiveExpr
              | shiftExpr RSHIFT additiveExpr
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
    return p

def p_additiveExpr(p):
    '''
    additiveExpr : additiveExpr PLUS multiplicativeExpr
                 | additiveExpr MINUS multiplicativeExpr
                 | multiplicativeExpr

    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
    return p

def p_multiplicativeExpr(p):
    '''
    multiplicativeExpr : multiplicativeExpr TIMES castExpr
                       | multiplicativeExpr DIVIDE castExpr 
                       | multiplicativeExpr MODULO castExpr   
                       | operand
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 4):
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
    else: 
        pass 
    return p

def p_castExpr(p):
    '''
    castExpr : unaryExpr 
             | LPAREN typeSpec RPAREN castExpr 
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else: 
        p[0] = '(' + str(p[2]) +')' + str(p[1])
    return p    

# Any unary operator and casting are not supported together.
def p_unaryExpr(p):
    '''
    unaryExpr : postfixExpr
              | INCREMENT unaryExpr
              | DECREMENT unaryExpr
              | SIZEOF LPAREN unaryExpr RPAREN
              | SIZEOF LPAREN typeSpec RPAREN
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = '(' + str(p[1]) + ')' + str(p[2])
    else:
        p[0] = str(p[3])
    return p


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
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = '(' + str(p[1]) + ')' + str(p[2])
    elif (len(p) == 4):
        p[0] = '(' + str(p[1]) + ',' + str(p[3] )+ ')' + str(p[2])
    elif (len(p) == 5):
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')'
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
    
# TODO: Add other types
def p_returnStmt(p):
    '''
    returnStmt : RETURN expr
               | RETURN varAssign
               | RETURN funcCall
    '''
    
    p[0] = str(p[1]) + '-' + str(p[2])
    return p

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

    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = str(p[1]) + ',' + str(p[2]) 
    elif (len(p) == 4):
        p[0] = '(' + str(p[2]) + ',' + str(p[3]) + ')' + str(p[1]) 
    elif (len(p) == 5):
        p[0] = '(' + str(p[3]) + ',' + str(p[4]) + ')' + str(p[1])+'-'+str(p[2])
    
    return p

def p_varDeclList(p):
    '''
    varDeclList : varDeclList varDecl SEMI
                | varDecl SEMI
    '''
    if (len(p) == 4):
        p[0] =  str(p[1])  + ',' + '(' +  str(p[2]) + ')'
    else:
        p[0] = '(' +  str(p[1]) + ')'
    return p
    
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
    p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
    return p


def p_typeSpecList(p):
    '''
    typeSpecList : typeSpecList COMMA typeSpec ID
                 | typeSpec ID
    '''
    if(len(p) == 3):
        p[0] = str(p[2]) + ',' + str(p[1])
    else:
        p[0] =  p[1] + ',' + '(' + str(p[3]) + ',' + str(p[4]) + ')' 
    return p

def p_idList(p):
    '''
    idList : idList COMMA ID
           | ID
    '''
    if (len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = p[1] + ',' + str(p[3])

#TOTAKECAREOF: register keyword can only be used within scope
# global variables are not allowed yet
# typedef not working yet
# Extern keyword can not have definition. That's why varDecl
# has EXTERN 
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
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3): 
        p[0] = str(p[1]) +'-'+ str(p[2])
    elif (len(p) == 4):
        p[0] = str(p[1]) +'-'+ str(p[2]) + '-' + str(p[3]) 
    return p

def p_combineTypeSpec(p):
    '''
    combineTypeSpec : combineType LBRACE varDeclList RBRACE
    '''
    if (len(p) == 5):
        p[0] = '(' + str(p[3]) + ')' + str(p[1])
    return p

def p_combineType(p):
    '''
    combineType : STRUCT ID
                | UNION ID
    '''
    p[0] = str(p[1]) +'-'+ str(p[2])
    return p

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
        p[0] = str(p[1]) + '-' + str(p[2])
    else: 
        p[0] = str(p[1]) + '-' + str(p[2]) + '-' + str(p[3])
    return p

def p_gotoStmt(p):
    '''
    gotoStmt : GOTO ID 
    '''
    p[0] = 'goto' + '-' + str(p[2])
    return p
    
def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN conditionals RPAREN scope
           | IF LPAREN conditionals RPAREN scope elseIfList
    '''
    if (len(p) == 6):
        p[0] = '(' + '(' + str(p[3]) + ',' + str(p[5]) + ')' + 'if' + ')ifstmt'
    else: 
        p[0] = '(' + '(' + str(p[3]) + ',' + str(p[5]) + ')' + 'if' + ',' + str(p[6]) + ')ifstmt'

    return p
        
def p_elseIfList(p):
    '''
    elseIfList : ELSE IF LPAREN conditionals RPAREN scope elseIfList
               | ELSE IF LPAREN conditionals RPAREN scope
               | ELSE scope     
    '''
    if(len(p) == 3):
        p[0] = '(' + str(p[2]) + ')else'
    elif (len(p) == 7):
        p[0] = '(' + str(p[4]) + ',' + str(p[6]) + ')elsif'
    elif (len(p) == 8):
        p[0] = '(' + str(p[4]) + ',' + str(p[6]) + ')elsif' + ',' + p[7]
    return p

def p_scope(p):
    '''
    scope : LBRACE statementList RBRACE
    '''
    p[0] = '(' + str(p[2]) + ')' + 'stmt'
    return p

def p_args(p):
    '''
    args : typeSpecList
         | idList
         | empty
    '''
    p[0] = '(' + str(p[1]) + ')' + 'args'
    return p

def p_program(p):
    '''
    program : funcList
    '''
    p[0] = p[1]
    return p

def p_funcDeclaration(p):
    '''
    funcList : typeSpec ID LPAREN args RPAREN scope funcList
             | typeSpec ID LPAREN args RPAREN scope
    '''
    typeSpecID = str(p[2] + '"' + p[1] + '"')
    arg = str(p[4])
    scope = str(p[6])

    if (len(p) == 7):
        p[0] = '(' + arg + ',' + scope + ')' +  typeSpecID
    else:
        p[0] = '(' + arg + ',' + scope + ')' +  typeSpecID + ',' + p[7]
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
        p[0] = p[2]
    return p

def p_whileLoop(p):
    '''
    whileLoop : WHILE LPAREN conditionals RPAREN scope
    '''
    p[0] = '(' + str(p[3]) + ',' + str(p[5]) + ')while'
    return p

def p_doWhile(p):
    '''
    doWhile : DO scope WHILE LPAREN conditionals RPAREN
    '''
    p[0] = '(' + str(p[2]) + ',' + str(p[5]) + ')doWhile'

    return p

def p_forInit(p):
    '''
    init : typeSpec varAssign
         | varAssign
    '''
    if(len(p) == 3):
        p[0] = str(p[1]) + ',' + str(p[2])
    else:
        p[0] = p[1]
    return p

def p_forIncrement(p):
    '''
    increment : varAssign
              | INCREMENT ID
              | DECREMENT ID
              | ID INCREMENT
              | ID DECREMENT 
    '''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = str(p[1]) + ',' + str(p[2])
    return p


def p_forLoop(p):
    '''
    forLoop : FOR LPAREN empty SEMI compOps SEMI empty RPAREN scope
            | FOR LPAREN init SEMI compOps SEMI empty RPAREN scope
            | FOR LPAREN empty SEMI compOps SEMI increment RPAREN scope
            | FOR LPAREN init SEMI compOps SEMI increment RPAREN scope
    '''
    p[0] = '(' + '(' + '(' + str(p[3]) + ')' + 'init)' + ',' + '(' + '(' + str(p[5]) + ')' + 'test)' + ',' + '(' + '(' + str(p[7]) + ')' + 'increment)' + ',' + str(p[9]) + ')forLoop'
    return p

def p_breakStmt(p):
    '''
    breakStmt : BREAK
    '''
    p[0] = p[1]
    return p

def p_caseList(p):
    '''
    caseList : CASE operand COLON statementList caseList
             | CASE CHARACTER COLON statementList caseList
             | CASE operand COLON statementList 
             | CASE CHARACTER COLON statementList 
             | DEFAULT COLON statementList
    '''
    case = 'case' + '-' + str(p[2])
    if(len(p) == 6):
        p[0] = '(' + str(p[4]) + ')'+ case + ',' +  str(p[5])
    if(len(p) == 5):
        p[0] = '(' + str(p[4]) + ')'+ case
    if(len(p) == 4):
        p[0] = '(' + str(p[3]) + ')'+ 'default'
    return p
    
def p_switchScope(p):
    '''
    switchscope : LBRACE caseList RBRACE
    '''
    p[0] = '(' + str(p[2]) + ')cases'
    return p

def p_switch(p):
    '''
    switch : SWITCH LPAREN expr RPAREN switchscope 
    '''
    p[0] = '(' + str(p[3]) + ',' + str(p[5]) + ')switch'
    return p

def p_error(t):
    print("Syntax error at {0}: Line Number: {1}".format(t.value, t.lineno))
    #print("Syntax error at '%s'" % t.value)

# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    result = parser.parse(lexer=lex)
    print(result)
    s = '(' + str(result) + ')Program;'
    return s