program         : declarationList
declarationList : declarationList declaration | declaration
declaration     : PREPROC  | varDecl SEMI | enumDeclaration
enumDeclaration : funcList | ENUM ID LBRACE enumArgs RBRACE SEMI
                | ENUM LBRACE enumArgs RBRACE SEMI | ENUM ID SEMI
enumArgs        : enumIDList | enumArgs COMMA enumIDList
enumIDList      : ID | ID EQUALS NUMCONST


funcList        : typeSpec ID LPAREN args RPAREN scope
args            : typeSpecList | operandList | empty
operandList     : operandList COMMA operand | operand
operand         : ID | NUMCONST | funcCall | LPAREN expr RPAREN | MINUS NUMCONST
scope           : LBRACE statementList RBRACE


varDeclList     : varDeclList varDecl SEMI | varDecl SEMI
varDecl         : combineTypeSpec | typeSpec ID | typeSpec varAssign
                | combineTypeSpec ID | TYPEDEF typeSpec ID | TYPEDEF combineTypeSpec ID
                | EXTERN typeSpecPostfix ID | CONST EXTERN typeSpecPostfix ID
typeSpecList    : typeSpecList COMMA typeSpec ID | typeSpec ID
typeSpec        : AUTO typeSpecPostfix | VOLATILE typeSpecPostfix
                | VOLATILE STATIC typeSpecPostfix | STATIC typeSpecPostfix
                | CONST typeSpecPostfix | REGISTER typeSpecPostfix
                | REGISTER STATIC typeSpecPostfix | typeSpecPostfix
                | combineType
combineTypeSpec : combineType LBRACE varDeclList RBRACE
combineType     : STRUCT ID | UNION ID
typeSpecPostfix : INT | CHAR | SHORT | LONG | FLOAT | DOUBLE | UNSIGNED INT | SIGNED INT | SHORT INT | LONG INT
                | LONG LONG INT | UNSIGNED CHAR | SIGNED CHAR | LONG LONG | SIGNED LONG | UNSIGNED LONG  
                | LONG DOUBLE | SIGNED SHORT | UNSIGNED SHORT 


statementList   : empty | statement SEMI statementList 
                | whileLoop statementList | switch statementList
                | ifStmt statementList | forLoop statementList
statement       : returnStmt | varDecl | varAssign | gotoStmt
                | expr | empty | doWhile
whileLoop       : WHILE LPAREN conditionals RPAREN loopScope
loopScope       : LBRACE loopStatementList RBRACE 
loopStatementList: breakStmt SEMI loopStatementList
                | continueStmt SEMI loopStatementList
                | statementList

ifStmt          : IF LPAREN conditionals RPAREN scope
                | IF LPAREN conditionals RPAREN scope elseIfList
elseIfList      : ELSE IF LPAREN conditionals RPAREN scope elseIfList
                | ELSE IF LPAREN conditionals RPAREN scope
                | ELSE scope  
doWhile         : DO scope WHILE LPAREN conditionals RPAREN
forLoop         : FOR LPAREN empty SEMI compOps SEMI empty RPAREN loopScope
                | FOR LPAREN init SEMI compOps SEMI empty RPAREN loopScope
                | FOR LPAREN empty SEMI compOps SEMI increase RPAREN loopScope
                | FOR LPAREN init SEMI compOps SEMI increase RPAREN loopScope
init            : typeSpec varAssign | varAssign
increase        : varAssign | INCREMENT ID | DECREMENT ID | ID INCREMENT | ID DECREMENT 
switch          : SWITCH LPAREN expr RPAREN switchscope 
switchscope     : LBRACE caseList RBRACE
caseList        : CASE operand COLON statementList caseList
                | CASE CHARACTER COLON statementList caseList
                | CASE operand COLON statementList 
                | CASE CHARACTER COLON statementList 
                | DEFAULT COLON statementList
returnStmt      : RETURN expr | RETURN varAssign
gotoStmt        : GOTO ID 
breakStmt       : BREAK
continueStmt    : CONTINUE
funcCall        : ID LPAREN args RPAREN


expr            : logicalExpr
logicalExpr     : compOps | logicalExpr LOR compOps
                | logicalExpr LAND compOps | logicalExpr OR compOps
                | logicalExpr XOR compOps  | logicalExpr AND compOps
compOps         : shiftExpr | compOps EQ shiftExpr 
                | compOps NE shiftExpr | compOps LE shiftExpr
                | compOps GE shiftExpr | compOps LANGLE shiftExpr
                | compOps RANGLE shiftExpr 
shiftExpr       : additiveExpr | shiftExpr LSHIFT additiveExpr
                | shiftExpr RSHIFT additiveExpr
additiveExpr    : additiveExpr PLUS multiplicativeExpr | additiveExpr MINUS multiplicativeExpr 
                | multiplicativeExpr
multiplicativeExpr : multiplicativeExpr TIMES castExpr | multiplicativeExpr DIVIDE castExpr  
                | multiplicativeExpr MODULO castExpr | castExpr
castExpr        : unaryExpr | LPAREN typeSpec RPAREN castExpr 
unaryExpr       : postfixExpr | LNOT unaryExpr | NOT unaryExpr
                | SIZEOF LPAREN unaryExpr RPAREN | SIZEOF LPAREN typeSpec RPAREN
                | unaryExpr INCREMENT | unaryExpr DECREMENT
postfixExpr     : operand  | postfixExpr PERIOD ID
                | postfixExpr LBRACKET expr RBRACKET
                | INCREMENT postfixExpr | DECREMENT postfixExpr  
varAssign       : ID EQUALS expr | ID EQUALS STRING | LPAREN varAssign RPAREN
                | ID TIMESEQUAL expr | ID DIVEQUAL expr | ID MODEQUAL expr 
                | ID PLUSEQUAL expr  | ID MINUSEQUAL expr | ID LSHIFTEQUAL expr 
                | ID RSHIFTEQUAL expr | ID ANDEQUAL expr | ID OREQUAL expr 
                | ID XOREQUAL expr      
conditionals    : expr | TRUE | FALSE  | LPAREN conditionals RPAREN        


