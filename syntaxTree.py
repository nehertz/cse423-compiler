# The astConstruct function recieves argument p, and constructs the AST
# p is a sequence containing the values of each grammar symbol in the corresponding rule.
# we can direcly use p[i] to retrieve the corresponding grammar symbol's value
# Accoding to the different token types, we can construct the ast and output the
# Tree structure in newick format.
# The values of p[i] are mapped to grammar symbols as shown here:
# program : declarationList
#   p[0]  =     p[1]


def astConstruct(p, type):
    if(type == 'program' or type == 'statement' or type == 'declaration' or type == 'expr' or type == 'breakStmt' or type == 'continueStmt'):
        p[0] = p[1]
    
    elif (type == 'operand'):
        if(len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 3):
            if (p[1] == '-'):
                # p[0] = '"' + str(p[1]) + str(p[2]) + '"'
                p[0] = '(' + str(p[2]) + ')' + str(p[1])
            else:
                p[0] = p[1]
        else:
            p[0] = p[2]

    elif(type == 'declarationList'):
        if(len(p) == 2):
            p[0] = p[1]
        else:
            # p[0] = p[1]  +  ',' + '(' + p[2] + ')'
            p[0] = p[1] + ',' + p[2]

    elif (type == 'enumInScope'):
        # p[0] = str(p[1]) + ',' + str(p[2]) + ',' + str(p[3])
        p[0] = '(' + str(p[3]) + ')' + str(p[1]) + '-' + str(p[2])

    elif (type == 'enumDeclaration'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 7):
            p[0] = '(' + str(p[4]) + ')' +  str(p[1]) + '-' + str(p[2])
        elif (len(p) == 6):
            p[0] = '(' + str(p[3]) + ')' +  str(p[1])
        elif (len(p) == 5):
            p[0] = '(' + str(p[3]) + ')' +  str(p[1]) + '-' + str(p[2])
        else:
            pass

    elif (type == 'enumArgs'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 4):
            p[0] = str(p[1]) + ' , ' + str(p[3])
        else:
            pass

    elif (type == 'enumIDList'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 4):
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
        else:
            pass

    elif(type == 'funcList'):
        typeSpecID = 'func-' + str(p[2])
        arg = str(p[5])
        scope = str(p[8])
        p[0] = '(' + arg + ',' + scope + ')' + typeSpecID

    elif(type == 'args'):
        p[0] = '(' + str(p[1]) + ')' + 'args'

    elif(type == 'operandList'):
        if (len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = str(p[1]) + ',' + str(p[3])

    elif(type == 'idList'):
        if (len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = str(p[1]) + ',' + str(p[3])

    elif(type == 'scope' or type == 'conditionalScope'):
        p[0] = '(' + str(p[3]) + ')' + 'stmt'

    elif(type == 'varDeclList'):
        if (len(p) == 4):
            p[0] = '(' + str(p[1]) + ',' + str(p[2]) + ')'
        else:
            p[0] = str(p[1])

    elif(type == 'varDecl'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 3):
            #p[0] = str(p[1]) + ',' + str(p[2])
            p[0] = '(' + str(p[2]) + ')varDecl'
        elif (len(p) == 4):
            if (str(p[3]) == 'None'):
                p[0] = str(p[2])
            else:
                p[0] = '(' + str(p[3]) + ')varDecl'
            # if (p[1] == 'TYPEDEF' or p[1] == 'EXTERN'):
            #     p[0] = '(' + str(p[2]) + ',' + str(p[3]) + ')' + str(p[1])
            # elif (str(p[3]) == 'None'):
            #     p[0] = str(p[2])
        elif (len(p) == 5):
            if (p[1] == 'CONST'):
                p[0] = '(' + str(p[4]) + ')varDecl'
        elif (len(p) == 7):
            p[0] = '(' + str(p[2]) + ')varDecl' + ',' + str(p[5])

    elif (type == 'varCommaList'):
        if (len(p) == 2):
             p[0] = '(' + str(p[1]) + ')varDecl'
        else:
            p[0] = '(' + str(p[1]) + ')varDecl' + ',' + str(p[3])

    elif(type == 'typeSpecList'):
        if(len(p) == 3):
            # p[0] ='(' + str(p[1]) + ',' + str(p[2]) + ')'
            p[0] = str(p[2])
        else:
            p[0] = p[1] + ',' + str(p[4])

    elif(type == 'typeSpec'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 3):
            p[0] = str(p[1]) + '-' + str(p[2])
        elif (len(p) == 4):
            p[0] = str(p[1]) + '-' + str(p[2]) + '-' + str(p[3])

    elif(type == 'combineTypeSpec'):
        p[0] = '(' + str(p[3]) + ')' + str(p[1])

    elif(type == 'combineType'):
        p[0] = str(p[1]) + '-' + str(p[2])

    elif(type == 'typeSpecPostfix'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 3):
            p[0] = str(p[1]) + '-' + str(p[2])
        else:
            p[0] = str(p[1]) + '-' + str(p[2]) + '-' + str(p[3])

    elif(type == 'statementList'):
        if(len(p) == 4 and p[3] != None):
            # p[0] = '(' + str(p[1]) + ')' + ',' + str(p[3])
            p[0] = str(p[1]) + ',' + str(p[3])
        elif(len(p) == 3 and p[2] != None):
            #p[0] = '(' + str(p[1]) + ')'  + ',' + str(p[2])
            p[0] = str(p[1]) + ',' + str(p[2])
        else:
            p[0] = p[1]

    elif(type == 'whileLoop'):
        p[0] = '(' + '(' + str(p[3]) + ')condition' +  ',' + '(' + str(p[5]) + ')stmt' + ')while'

    elif(type == 'ifStmt'):
        if (len(p) == 6):
            p[0] = '(' + '(' + str(p[3]) + ',' + str(p[5]) + ')' + 'if' + ')condStmt'
        else: 
            p[0] = '(' + '(' + str(p[3]) + ',' + str(p[5]) + ')' + 'if' + ',' + str(p[6]) + ')condStmt'

    elif(type == 'elseIfList'):
        if(len(p) == 3):
            p[0] = '(' + str(p[2]) + ')else'
        elif (len(p) == 7):
            p[0] = '(' + str(p[4]) + ',' + str(p[6]) + ')else-if'
        elif (len(p) == 8):
            p[0] = '(' + str(p[4]) + ',' + str(p[6]) + ')else-if' + ',' + p[7]

    elif(type == 'doWhile'):
        # p[0] = '(' + str(p[2]) + ',' + str(p[5]) + ')doWhile'
        p[0] = '(' + '(' + str(p[5]) + ')condition' + ',' + '(' + str(p[2]) + ')stmt' + ')dowhile'

    elif(type == 'forLoop'):
        # p[0] = '(' +  '(' + str(p[3]) + ')' + 'init' + ',' + '(' + str(p[5]) + ')' + \
        #     'condition' + ',' + \
        #     '(' + str(p[7]) + ')' + 'increment' + \
        #     ',' + '(' + str(p[9]) + ')stmt' + ')forLoop'

        p[0] = '(' + '(' + str(p[9]) + ')stmt' + \
            ',' + '(' + str(p[3]) + ')init' +\
            ',' + '(' + str(p[7]) + ')increment' + \
            ',' + '(' + str(p[5]) + ')condition' + ')forLoop'

    elif(type == 'init'):
        if(len(p) == 3):
            p[0] = str(p[2])
        else:
            p[0] = p[1]

    elif(type == 'increment'):
        if(len(p) == 2):
            p[0] = p[1]

    elif(type == 'switch'):
        p[0] = '(' + str(p[3]) + ',' + str(p[5]) + ')switch'

    elif(type == 'switchscope'):
        p[0] = '(' + str(p[2]) + ')cases'

    elif(type == 'caseList'):
        case = 'case' + '-' + str(p[2])
        if(len(p) == 6):
            p[0] = '(' + str(p[4]) + ')' + case + ',' + str(p[5])
        if(len(p) == 5):
            p[0] = '(' + str(p[4]) + ')' + case
        if(len(p) == 4):
            p[0] = '(' + str(p[3]) + ')' + 'default'

    elif(type == 'returnStmt'):
        p[0] = '(' + str(p[2]) + ')' + str(p[1])

    elif(type == 'gotoStmt'):
        p[0] =  '(' + str(p[2]) + ')' + 'goto'

    elif(type == 'labeledStmt'):
        p[0] = '(' + str(p[1]) + ')' + 'label'

    elif(type == 'funcCall'):
        p[0] = '(' + str(p[3]) + ')' + 'func-' + str(p[1])

    elif(type == 'logicalExpr'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 4):
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
        elif (len(p) == 5):
            p[0] = '(' + str(p[1]) + ',' + str(p[4]) + ')' + str(p[2])

    elif(type == 'compOps'):
        if (len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])

    elif(type == 'shiftExpr'):
        if (len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])

    elif(type == 'additiveExpr'):
        if (len(p) == 2):
            p[0] = p[1]
        else:
            # p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + '"'+ str(p[2]) + '"'
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])

    elif(type == 'multiplicativeExpr'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (len(p) == 4):
            #p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + '"'+ str(p[2]) + '"'
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])

        else:
            pass

    elif(type == 'castExpr'):
        if (len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = '(' + str(p[2]) + ',' + str(p[4]) + ')cast'

    # TODO: Remove Quotation marks
    elif(type == 'unaryExpr'):
        if (len(p) == 2):
            p[0] = p[1]
        elif (p[2] == '++'):
            p[0] = '(' + str(p[1]) + ')++'
        elif (p[2] == '--'):
            p[0] = '(' + str(p[1]) + ')--'

        elif (p[1] == '!' or p[1] == '~'):
            p[0] = '(' + p[2] + ')' + p[1]
            # p[0] = str(p[1]) + str(p[2])
        elif (len(p) == 3):
            # p[0] = '(' + str(p[1]) + ')' + str(p[2])
            p[0] = str(p[1]) + str(p[2])
        elif (len(p) == 5):
            # p[0] = '(' +  str(p[3]) + ')' + str(p[1])
            p[0] = str(p[1]) + '-' + str(p[3])
        else:
            p[0] = str(p[3])

    elif(type == 'postfixExpr'):
        if (len(p) == 2):
            p[0] = p[1]

        elif (p[1] == '++'):
            p[0] = '(' + str(p[2]) + ')++'
        elif (p[1] == '--'):
            p[0] = '(' + str(p[2]) + ')--'

        elif (len(p) == 3):
            p[0] = '(' + '"' + str(p[1]) + '"' + ')' + str(p[2])
        elif (len(p) == 4):
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
        elif (len(p) == 5):
            p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')'
        else:
            pass

    elif(type == 'varAssign'):
        p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + str(p[2])
        # p[0] = '(' + str(p[1]) + ',' + str(p[3]) + ')' + 'ASSIGN'

    elif(type == 'conditionals'):
        if (len(p) == 2):
            p[0] = str(p[1])
        elif (len(p) == 4):
            p[0] = str(p[2])

    elif (type == 'loopScope'):
        p[0] = str(p[3])

    elif (type == 'loopStatementList'):
        if (len(p) == 4):
            p[0] = str(p[1]) + ',' + str(p[3])
        else:
            p[0] = str(p[1])

    else:
        print("AST error, {0} is missing".format(type))
    return p
