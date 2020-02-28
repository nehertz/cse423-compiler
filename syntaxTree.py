from treeNode import Node
# The astConstruct function recieves argument p, and constructs the AST
# p is a sequence containing the values of each grammar symbol in the corresponding rule. 
# we can direcly use p[i] to retrieve the corresponding grammar symbol's value 
# Accoding to the different token types, we can construct the ast and output the 
# Tree structure in newick format. 
# The values of p[i] are mapped to grammar symbols as shown here:
# program : declarationList
#   p[0]  =     p[1]

def astConstruct(p, type):
    if(type == 'program'):
        p[0] = Node(p[1], 'program')
        print(p[0])
        return p[0]

    elif(type == 'declaration'):
        p[0] = Node(p[1])

    elif(type == 'statement'):
        p[0] = Node(p[1])

    elif(type == 'expr'):
        p[0] = Node(p[1])

    elif(type == 'breakStmt'):
        p[0] = Node(leaf='break')
        
    elif(type == 'continueStmt'):
        p[0] = Node(leaf='continue') 
        
    # FIXME: Might need to split up operand to make it feasible to print
    elif (type == 'operand'):
        if(len(p) == 2):
            p[0] = Node(p[1]) 
        elif (len(p) == 3):
            node = '"' + p[1] + p[2] + '"'
            p[0] = Node(node)
        else:
            p[0] = Node(p[2]) 

    elif(type == 'declarationList'):
        if(len(p) == 2):
            p[0] = Node(p[1])
        else:
            p[0] = Node([p[1],p[2]])
            #p[0] = p[1]  +  ',' + '(' + p[2] + ')'
    
    elif (type == 'enumInScope'):
        p[0] = Node(leaf=('enum ' + p[2] + ' ' + p[3]))
        #p[0] = p[1] + ',' + p[2] + ',' + p[3]

    elif (type == 'enumDeclaration'):
        if (len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        elif (len(p) == 7):
            p[0] = Node([p[4]], 'enum ' + p[2])
           # p[0] = p[1] + ',' + p[4]
        elif (len(p) == 6):
            p[0] = Node([p[3]], 'enum')
            #p[0] = p[1] + ',' + p[3]
        elif (len(p) == 5):
            p[0] = Node(leaf=('enum ' + p[2] + ' ' + p[3]))
            #p[0] = p[1] + ',' + p[2]
        else: 
            pass

    elif (type == 'enumArgs'):
        if (len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        elif (len(p) == 4):
            p[0] = Node([p[1], p[3]])
            #p[0] = p[1] + ' , ' + p[3]
        else: 
            pass

    elif (type == 'enumIDList'):
        if (len(p) == 2):
            p[0] = Node(leaf=p[1])
            #p[0] = p[1]
        elif (len(p) == 4):
            p[0] = Node(leaf=p[1] + ' ' + p[2] + ' ' + p[3])
            #p[0] = '(' + p[1] + ',' + p[3] + ')' + p[2]
        else:
            pass

    elif(type == 'funcList'):
        typeSpecID = str(p[1]) + ' ' + str(p[2])
        # arg = p[4]
        # scope = p[6]
        p[0] = Node([p[4], p[6]], typeSpecID)
        #p[0] = '(' + arg + ',' + scope + ')' +  typeSpecID

    elif(type == 'args'):
        p[0] = Node(p[1], 'args')
       # p[0] = '(' + p[1] + ')' + 'args'

    elif(type == 'operandList'):
        if (len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        else:
            p[0] = Node([p[1],p[3]])
            #p[0] = p[1] + ',' + p[3]

    # FIXME: I don't think this grammar rule exists anymore
    elif(type == 'idList'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        else:
            p[0] = Node([p[1],p[3]])
           # p[0] = p[1] + ',' + p[3]
        
    elif(type == 'scope' or type == 'conditionalScope'):
        p[0] = Node(p[3], 'scope')
       # p[0] = '(' + p[2] + ')' + 'stmt'

    elif(type == 'varDeclList'):
        if (len(p) == 4):
            p[0] = Node([p[1], p[2]])
            #p[0] =  '(' + p[1]  + ','  +  p[2] + ')'
        else:
            p[0] = Node(p[1])
            #p[0] = p[1] 

    elif(type == 'varDecl'):
        if (len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        elif (len(p) == 3):
            p[0] = Node(leaf=p[1] + ' ' + p[2])
            #p[0] = p[1] + ',' + p[2] 
        elif (len(p) == 4):
            p[0] = Node(leaf=p[1] + ' ' + p[2] + ' ' + p[3])
            #p[0] = '(' + p[2] + ',' + p[3] + ')' + p[1] 
        elif (len(p) == 5):
            p[0] = Node(leaf=p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4])
            #p[0] = '(' + p[3] + ',' + p[4] + ')' + p[1]+'-'+p[2]

    elif(type == 'typeSpecList'):
        if(len(p) == 3):
            p[0] = Node(leaf=p[1] + ' ' + p[2])
            #p[0] ='(' + p[1] + ',' + p[2] + ')'
        else:
            p[0] = Node([p[1]], p[3] + ' ' + p[4])
            #p[0] =  p[1] + ',' + '(' + p[3] + ',' + p[4] + ')' 

    elif(type == 'typeSpec'):
        if (len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        elif (len(p) == 3): 
            p[0] = Node(p[2], p[1])
            #p[0] = p[1] +'-'+ p[2]
        elif (len(p) == 4):
            p[0] = Node(p[3], str(p[1] + ' ' + p[2]))
            #p[0] = p[1] +'-'+ p[2] + '-' + p[3]

    elif(type == 'combineTypeSpec'):
        p[0] = Node(p[3], p[1])
        #p[0] = '(' + p[3] + ')' + p[1]

    elif(type == 'combineType'):
        p[0] = Node(leaf=p[1] + ' ' + p[2])
        #p[0] = p[1] +'-'+ p[2]

    elif(type == 'typeSpecPostfix'):
        if (len(p) == 2):
            p[0] = Node(leaf=p[1])
            #p[0] = p[1]
        elif (len(p) == 3):
            p[0] = Node(leaf=str(p[1] + ' ' + p[2]))
            #p[0] = p[1] + '-' + p[2]
        # else: 
        #     p[0] = Node(p[1] +'-'+ p[2] + '-' + p[3])
        #     #p[0] = p[1] + '-' + p[2] + '-' + p[3]

    elif(type == 'statementList'):
        # if(len(p) == 4 and p[3] != None):
        #      p[0] = Node(p[1], p[3])
        #     #p[0] = '(' + p[1] + ')' + ',' + p[3] 
        # elif(len(p) == 3 and p[2] != None):
        #      p[0] = Node(p[1], p[2])
        #     #p[0] = '(' + p[1] + ')'  + ',' + p[2]
        # else:
        #     p[0] = Node(p[1])
        #     #p[0] = p[1]
        if (len(p) == 4):
            p[0] = Node(leaf=str(p[1]) + ' ' + str(p[3]))
        elif (len(p) == 3):
            p[0] = Node(p[3], p[1])
        else:
            pass
        
    elif(type == 'whileLoop'):
        p[0] = Node([p[3], p[5]], 'while')
        #p[0] = '(' + p[3] + ',' + p[5] + ')while'

    elif(type == 'ifStmt'):
        if (len(p) == 6):
            p[0] = Node([p[3], p[5]], 'if')
            #p[0] = '(' + '(' + p[3] + ',' + p[5] + ')' + 'if' + ')ifstmt'
        else: 
            p[0] = Node([p[3], p[5], p[6]], 'if')
            #p[0] = '(' + '(' + p[3] + ',' + p[5] + ')' + 'if' + ',' + p[6] + ')ifstmt'

    elif(type == 'elseIfList'):
        if(len(p) == 3):
            p[0] = Node(p[2], 'else')
            #p[0] = '(' + p[2] + ')else'
        elif (len(p) == 7):
            p[0] = Node([p[4],p[6]], 'else if')
            #p[0] = '(' + p[4] + ',' + p[6] + ')elsif'
        elif (len(p) == 8):
            p[0] = Node([p[4],p[6],p[7]], 'else if')
            #p[0] = '(' + p[4] + ',' + p[6] + ')elsif' + ',' + p[7]

    elif(type == 'doWhile'):
        p[0] = Node([p[2],p[5]], 'do while')
        #p[0] = '(' + p[2] + ',' + p[5] + ')doWhile'

    elif(type == 'forLoop'):
        p[0] = Node([p[3],p[5], p[7], p[9]], 'for')
        #p[0] = '(' + '(' + '(' + p[3] + ')' + 'init)' + ',' + '(' + '(' + p[5] + ')' + 'test)' + ',' + '(' + '(' + p[7] + ')' + 'increment)' + ',' + p[9] + ')forLoop'

    elif(type == 'init'):
        if(len(p) == 3):
            p[0] = Node([p[1], p[2]])
            #p[0] = p[1] + ',' + p[2]
        else:
            p[0] = Node(p[1])
            #p[0] = p[1]

    elif(type == 'increment'):
        if(len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        else:
            p[0] = Node([p[1], p[2]])
            #p[0] = p[1] + ',' + p[2]

    elif(type == 'switch'):
        p[0] = Node([p[3], p[5]], 'switch')
        #p[0] = '(' + p[3] + ',' + p[5] + ')switch'

    elif(type == 'switchscope'):
        p[0] = Node(p[2], 'cases')
        #p[0] = '(' + p[2] + ')cases'

    elif(type == 'caseList'):
        case = 'case' + '-' + p[2]
        if(len(p) == 6):
            p[0] = Node([p[4], p[5]], 'case')    
           # p[0] = '(' + p[4] + ')'+ case + ',' +  p[5]
        if(len(p) == 5):
            p[0] = Node(p[4], 'case')    
            #p[0] = '(' + p[4] + ')'+ case
        if(len(p) == 4):
            p[0] = Node(p[3], 'default')  
            #p[0] = '(' + p[3] + ')'+ 'default'

    elif(type == 'returnStmt'):
        p[0] = Node([p[1], p[2]])
        #p[0] =  '(' + p[1] + ',' + p[2] + ')'

    elif(type == 'gotoStmt'):
         p[0] = Node(p[2], 'goto')
        #p[0] = 'goto' + '-' + p[2]

    elif(type == 'funcCall'):
        #p[0] = '(' + p[1] + ',' + p[3] + ')'
        p[0] = Node([p[1], p[3]])

    elif(type == 'logicalExpr'):
        if (len(p) == 2):
           #p[0] = p[1]
            p[0] = Node(p[1])
        else:
            p[0] = Node([p[1], p[3]], p[2])
            #p[0] = '(' + p[1] + ',' + p[3] + ')' + p[2]

    elif(type == 'compOps'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        else: 
            p[0] = Node([p[1], p[3]], p[2])
            #p[0] = '(' + p[1] + ',' + p[3] + ')' + p[2]

    elif(type == 'shiftExpr'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        else: 
            p[0] = Node([p[1], p[3]], p[2])
            #p[0] = '(' + p[1] + ',' + p[3] + ')' + p[2]

    elif(type == 'additiveExpr'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        else: 
            p[0] = Node([p[1], p[3]], p[2])
            #p[0] = '(' + p[1] + ',' + p[3] + ')' + '"'+ p[2] + '"'
        
    elif(type == 'multiplicativeExpr'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        elif (len(p) == 4):
            p[0] = Node([p[1], p[3]], p[2])
            #p[0] = '(' + p[1] + ',' + p[3] + ')' + '"'+ p[2] + '"'
        else: 
            pass 

    elif(type == 'castExpr'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        else: 
            p[0] = Node(p[2], p[1])
            #p[0] = '(' + p[2] +')' + p[1]

    elif(type == 'unaryExpr'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        elif (p[2] == '++' or p[2] == '--'):
            expression = '"' + p[1] + p[2] + '"'
            p[0] = Node(expression)
        elif (p[1] == '!' or p[1] == '~'):
            expression = '"' + p[1] + p[2] + '"'
            p[0] = Node(expression)
        elif (len(p) == 3):
            #p[0] = '(' + '"' + p[1] + '"' + ')' + p[2]
            p[0] = Node('"' + p[1] + '"', p[2])
        elif (len(p) == 5):
            p[0] = Node([p[1], ['"' + p[3] + '"']])
            #p[0] = '(' + p[1]  + '"' + p[3] + '"' + ')'
        else:
            p[0] = Node(p[3])
            #p[0] = p[3]

    elif(type == 'postfixExpr'):
        if (len(p) == 2):
            #p[0] = p[1]
            p[0] = Node(p[1])
        elif (p[1] == '++' or p[1] == '--'):
            expression = '"' + p[1] + p[2] + '"'
            p[0] = Node(expression)
        elif (len(p) == 3):
            #p[0] = '('  + '"' + p[1] + '"' + ')' +  p[2]
            p[0] = Node('"' + p[1] + '"', p[2])

        elif (len(p) == 4):
            p[0] = Node([p[1], p[3]], p[2])
            #p[0] = '(' + p[1] + ',' + str(p[3] )+ ')' + p[2]
        elif (len(p) == 5):
            #p[0] = '(' + p[1] + ',' + p[3] + ')'
            p[0] = Node([p[1], p[3]])
        else: 
            pass

    elif(type == 'varAssign'):
        #p[0] = '(' + p[1] + ',' + p[3] + ')' + p[2]
        p[0] = Node([p[1], p[3]], p[2])
    elif(type == 'conditionals'):
        if (len(p) == 2):
            p[0] = Node(p[1])
            #p[0] = p[1]
        elif (len(p) == 4):
            p[0] = Node(p[2])
            #p[0] = p[2]

    elif (type== 'loopScope'):
        p[0] = Node(p[2])
        #p[0] = p[2]
    
    elif (type == 'loopStatementList'):
        if (len(p) == 4):
            #p[0] = p[1] + ',' + p[3]
            p[0] = Node([p[1], p[3]], "scope")
        else:
            p[0] = Node([p[1]])

    else :
        print("AST error, {0} is missing".format(type))
    return p
