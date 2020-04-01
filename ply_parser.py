import ply.yacc as yacc
from ply_scanner import tokens
from skbio import read
from skbio.tree import TreeNode
from SymbolTable import SymbolTable
from syntaxTree import astConstruct
# from typeChecking import typeChecking
# Each grammar rule is defined by a Python function
# where the docstring to that function contains the
# appropriate context-free grammar specification.
# The statements that make up the function body implement
# the semantic actions of the rule.
# Each function accepts a single argument p
# that is a sequence containing the values of each
# grammar symbol in the corresponding rule.

# Specify the entry of the program
start = 'program'
st = SymbolTable()


def p_empty(p):
    'empty :'
    pass

# Grammar that defines start of the program
# the declaration list contains preprocessor, Global variable, enum and functions declartions
# The function passes argument p to AST construnction function.


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


# Grammar that defines function declaration
# the function should have type specifer, identifer, arguments
# scope represents everything that can exist in a function's scope
# funcList : typeSpec ID LPAREN parametersBegin args parametersEnd RPAREN scope
# funcList : typeSpec ID LPAREN args RPAREN scope

def p_funcDeclaration(p):
    '''
    funcList : typeSpec ID LPAREN parametersBegin args parametersEnd RPAREN scope

    '''
    st.symbolTableConstruct(p, 'funcDecl')
    return astConstruct(p, 'funcList')

def p_parametersBegin(p):
    '''
    parametersBegin :
    '''
    st.startFunctionParam()
    return p
    
def p_parametersEnd(p):
    '''
    parametersEnd   :
    '''
    st.endFunctionParam()
    return p

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
    operand : ID afterID
            | NUMCONST
            | funcCall
            | LPAREN expr RPAREN
            | MINUS NUMCONST

    '''
    return astConstruct(p, 'operand')


def p_afterID(p):
    '''
    afterID : 
    '''
    st.lookup(p[-1])
    return p


def p_scope(p):
    '''
    scope : LBRACE afterLBRACE statementList RBRACE afterRBRACE
    '''
    return astConstruct(p, 'scope')


def p_afterRBRACE(p):
    '''
    afterRBRACE :
    '''
    st.outScope()
    return p


def p_afterLBRACE(p):
    '''
    afterLBRACE :
    '''
    st.inScope()
    return p


def p_loopScope(p):
    '''
    loopScope : LBRACE afterLoopLBrace loopStatementList RBRACE afterLoopRBrace
    '''
    return astConstruct(p, 'loopScope')


def p_afterLoopLBrace(p):
    '''
    afterLoopLBrace : 
    '''
    st.loopInScope()
    return p


def p_afterLoopRBrace(p):
    '''
    afterLoopRBrace :
    '''
    st.loopOutScope()
    return p


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


# variable Declaration grammar
# The grammar specify a vaild variable declaration
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
            | typeSpec ID COMMA varCommaList
            | typeSpec varAssign afterVarAssign
            | combineTypeSpec ID    
            | TYPEDEF typeSpec ID
            | TYPEDEF combineTypeSpec ID
            | EXTERN typeSpecPostfix ID
            | CONST EXTERN typeSpecPostfix ID
    '''
    st.symbolTableConstruct(p, 'varDecl')
    return astConstruct(p, 'varDecl')

def p_varCommaList(p):
    '''
    varCommaList : ID COMMA varCommaList
                | ID 
    '''
    return astConstruct(p, 'varCommaList')


def p_afterVarAssign(p):
    '''
    afterVarAssign :
    '''
    st.symbolTable_afterVarAssign()
    return p

# TypeSpecifier Grammar


def p_typeSpecList(p):
    '''
    typeSpecList : typeSpecList COMMA typeSpec ID
                 | typeSpec ID
    '''
    st.symbolTableConstruct(p, 'typeSpecList')
    return astConstruct(p, 'typeSpecList')


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


# Statement Garmmars
# Statements include if-stmt, iteration stmts, switch stmts and enum stmts.
def p_statementList(p):
    '''
    statementList : empty
                  | statement SEMI statementList
                  | whileLoop statementList
                  | ifStmt statementList
                  | forLoop statementList
                  | switch statementList
                  | enumInScope statementList
                  | labeledStmt statementList
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


def p_whileLoop(p):
    '''
    whileLoop : WHILE LPAREN conditionals RPAREN loopScope
    '''
    return astConstruct(p, 'whileLoop')


def p_ifStmt(p):
    '''
    ifStmt : IF LPAREN conditionals RPAREN conditionalScope
           | IF LPAREN conditionals RPAREN conditionalScope elseIfList
    '''
    return astConstruct(p, 'ifStmt')


def p_elseIfList(p):
    '''
    elseIfList : ELSE IF LPAREN conditionals RPAREN conditionalScope elseIfList
               | ELSE IF LPAREN conditionals RPAREN conditionalScope
               | ELSE conditionalScope     
    '''
    return astConstruct(p, 'elseIfList')


def p_conditionalScope(p):
    '''
    conditionalScope : LBRACE afterLoopLBrace statementList RBRACE afterLoopRBrace
    '''
    return astConstruct(p, 'conditionalScope')


def p_doWhile(p):
    '''
    doWhile : DO loopScope WHILE LPAREN conditionals RPAREN
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
    init : varDecl
        | varAssign
    '''
    return astConstruct(p, 'init')


def p_forIncrement(p):
    '''
    increase : varAssign
              | expr
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

def p_labeledStmt(p):
    '''
    labeledStmt : ID COLON 
    '''
    return astConstruct(p, 'labeledStmt')

def p_funcCall(p):
    '''
    funcCall : ID LPAREN args RPAREN 
    '''
    return astConstruct(p, 'funcCall')


# Expression Grammars
# Includes grammars for logical, shift, arithmetic, and unary operations
# type cast is supported but Any unary operator and casting are not supported together.
# also included variable assign expression.
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


def p_unaryExpr(p):
    '''
    unaryExpr : postfixExpr
              | LNOT unaryExpr
              | NOT unaryExpr
              | MINUS unaryExpr
              | SIZEOF LPAREN unaryExpr RPAREN
              | SIZEOF LPAREN typeSpec RPAREN
              | unaryExpr INCREMENT
              | unaryExpr DECREMENT

    '''
    return astConstruct(p, 'unaryExpr')


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
    st.symbolTable_varAssign(str(p[1]))
    # s = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2]) + ';'
    # s = s.replace("\"", "")
    # print(s)
    # tc.checkTypes(s, st)
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
    # print(s)
    return s
