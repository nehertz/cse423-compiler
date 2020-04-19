'''
Class that handles the translation from the abstract syntax tree
to a linear 3-address intermediate representation of the original
source code.
'''

from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_scanner import assignment
from ply_scanner import operators
from ply_scanner import arithmetic
from ply_scanner import logical
from ply_scanner import comparison
from ply_scanner import alc

class IR:
    def __init__(self, ast):
        self.IRS = []
        self.queue = []
        self.enumConst = []
        self.labelPlace = {}
        self.enumList = {}
        self.enumInstance = {}
        if (ast != None):
            self.treeString = ast
            self.tree = TreeNode.read(StringIO(ast))

        self.temporaryVarible = 0
        self.label = 0
        self.enterLoopLabel = ''
        self.endLoopLabel = ''
        self.loopConditionLabel = ''
        self.ifLabel = []
        self.elifLabel = []
        self.elseLabel = []
        self.conditionLabel = []
        self.exitIFLabel = ''
        self.enterIFlabel = ''

    # Run function scans the first level of the AST and passes the node to other function 
    def run(self):
        for node in self.tree.children:
            # Handle function scope
            if ('func-' in str(node.name)):
                self.funcNode(node, node.name)
            # Handle enums
            elif ('enum-' in str(node.name)):
                pass
                # enumPair = self.enumDeclaration(node)
                # enumName = str(node.name).replace('enum-', '')
                # dict = {enumName : enumPair}
                # self.enumList.update(dict)
                # self.enumConst.append(enumPair)
                # print(enumConst)
            # Handle global variable declaration without assignment
            elif (node.name == 'varDecl'):
                self.varDecl(node)
            # Handle global variable declaration with assignment
            elif (node.name in assignment):
                self.assign(node)
            # else:
            #     print("Node ", node.name, " can not be converted")
        return self.IRS

    # Translates function name and arguments into IR
    # parameters: nodes, AST subtree with relevant parsed data
    # parameters: funcName, name of the function
    def funcNode(self, nodes, funcName):
        funcName = funcName.replace('func-', '')
        for node in nodes.children:
            if (node.name == 'args'):
                self.args(node, funcName, None)
            if (node.name == 'stmt'):
                self.statement(node)
        self.IRS.append(['}'])

    # Reads AST for function arguments and translates them into IR
    # parameters: nodes, AST subtree with relevant parsed data
    # parameters: funcName, name of the function
    # parameters: funcCallFlag, used to handle function call args
    # if funcCallFlag = 1，the args are from a function call instead of function definition
    # when funcCallFlag = 1, this function only enqueue the func call arguments and return
    # how many times it enqueues (the args count)
    def args(self, nodes, funcName, funcCallFlag):
        argsCount = 0
        ir = []
        if(funcCallFlag):
            for node in self.getSubtree(nodes):
                if (node.name != 'args' and node.name != None and node.name != funcName):
                    self.enqueue(node.name)
                    argsCount += 1
            return argsCount
        else:
            ir.append(funcName)
            for node in self.getSubtree(nodes):
                if (node.name != 'args' and node.name != None):
                    self.enqueue(node.name)
                    argsCount += 1
            ir.append('(')
            while argsCount > 0:
                ir.append(str(self.dequeue()))
                if argsCount != 1:
                    ir.append(',')
                argsCount -= 1
            ir.append(')')
            self.IRS.append(ir)
            self.IRS.append(['{'])

    # The statement function handles the statement body (scope) of functions, 
    # loops, and if-stmts
    # parameters: nodes, AST subtree with relevant parsed data
    # TODO: add IF-stmt and switch stmt. 
    def statement(self, nodes):
        for node in nodes.children:
            # convert var decl with assignment
            # int a = expr or a = expr
            if (node.name in assignment):
                self.assign(node)

            # convert the var-decl without assignment
            # Example: int a 
            elif (node.name == 'varDecl'):
                self.varDecl(node)

            # convert function calls.
            elif ('func-' in str(node.name)):
                self.funcCall(node, node.name, 0, 0)

            elif ('enum-' in str(node.name)):
                self.enumInst(node, node.name)
            # convert simple expressions
            # those are expressions without assignment
            # examples : '1 + 2 + 3', 'a << 1'
            # reference to scanner for the alc list,
            elif (node.name in alc):
                self.simpleExpr(node)

            elif (node.name == 'goto'):
                self.gotoStmt(node)

            elif (node.name == 'label'):
                self.createLabel(node, None)

            elif (node.name == 'return'):
                self.returnStmt(node)

            # convert increment and decrement, ++a and --a
            # the a = ++a case is handled by the assign() function
            elif (node.name == '++' or node.name == '--'):
                self.increment(node, node.name)

            elif (node.name == 'while'):
                self.whileloop(node)

            elif (node.name == 'dowhile'):
                self.dowhile(node)
            
            elif (node.name == 'forLoop'):
                self.forloop(node)

            elif (node.name == 'break'):
                self.breakStmt(node)

            elif (node.name == 'continue'):
                self.continueStmt(node)
            
            elif (node.name == 'ifstmt'):
                self.ifstmt(node)
            # else:
            #     print("Node ", node.name, " can not be converted")

    # Construct a dict structure to store an enum declaration
    # Key is the enum constant, value is the corresponding value of that constant
    # parameters: nodes, AST subtree with relevant parsed data
    def enumDeclaration(self, nodes):
        enumConst = {}
        value = 1
        for node in nodes.children:
            if (node.name != '=' ):
                dict = {node.name : value}
                enumConst.update(dict)
                value += 1
            elif (node.name == '='):
                enumName = str(node.children[0]).replace(';', '').replace('\n', '')
                value = node.children[1]
                value = int(str(value).replace(';', '').replace('\n', ''))
                dict = {enumName : value}
                enumConst.update(dict)
                value += 1
        return enumConst      

    # Bind the corresponding enum structure to the enum instance 
    # parameters: nodes, AST subtree with relevant parsed data
    # parameters: name, name of the enum
    def enumInst(self, nodes, name):
        eName = str(nodes.children[0]).replace(';', '').replace('\n', '')
        dict = self.enumList.get(str(name).replace('enum-', ''))
        dict = {eName : dict}
        self.enumInstance.update(dict)
    
    # Translate all assignment expression into IR
    # parameters: nodes, AST subtree with relevant parsed data
    def assign(self, nodes):
        subtree = self.getSubtree(nodes)
        operand2 = ''
        self.queue = []
        for node in reversed(subtree):
            if(node.name not in operators.keys() and 'func' not in node.name and node.name != 'args' and node.name != 'cast'):
                # Enqueue identifiers and constants
                self.enqueue(node.name)
            elif(node.name not in assignment and node.name in alc and node.name != '!' and len(node.children) != 1):
                # Handle logical or comparison operator
                operand2 = self.dequeue()
                operand1 = self.dequeue()
                operator = node.name
                flag = 1
                for enum in self.enumConst:
                    if (operand1 in enum):
                        tempVar = ['enumExpr', str(operand1) , str(operator) , str(operand2)]
                        self.enqueue(tempVar)
                        flag = 0
                if (flag):        
                    tempVar = 't_' + str(self.temporaryVarible)
                    ir = [tempVar, '=', operand1, operator, operand2]
                    self.IRS.append(ir)
                    self.enqueue(tempVar)
                    self.temporaryVarible += 1
            elif(node.name == '-' and len(node.children) == 1):
                # Handle negative number
                operand1 = self.dequeue()
                operator = node.name
                self.enqueue(operator+operand1)
            elif(node.name == '++' or node.name == '--'):
                # Handle increment and decrement
                operand1 = self.dequeue()
                operator = node.name[0]
                ir = [operand1, '=', operand1, operator, '1']
                self.IRS.append(ir)
                self.enqueue(operand1)
            elif(node.name == '!'):
                # Handle !
                operand1 = self.dequeue()
                operator = node.name
                self.enqueue(operator+operand1)
            elif('func' in node.name):
                # Handle function call
                ir = " ".join(self.funcCall(node, node.name, 0, 1))
                tempVar = 't_' + str(self.temporaryVarible)
                ir = [tempVar, '=', ir]
                self.enqueue(tempVar)
                self.IRS.append(ir)
                self.temporaryVarible += 1
            elif(node.name == 'cast'):
                # Handle type casting
                operand = self.dequeue() 
                typeSpec = self.dequeue()
                ir = '(' + str(typeSpec) + ')' +  str(operand)
                self.enqueue(ir)
            elif(node.name in assignment):
                # Handle assignment operators
                if(node.name == '='):
                    operand1 = self.dequeue()
                    operand2 = self.dequeue()
                    if (operand2 in self.enumInstance):
                        dict = self.enumInstance.get(operand2)
                        if ('enumExpr' in operand1):
                            value = dict.get(operand1[1])
                            value = self.simpleArithmetic(int(value), operand1[2], int(operand1[3]))
                        else :
                            value = dict.get(operand1)
                        ir = [operand2, '=', str(value)]
                        self.IRS.append(ir)
                    else:
                        ir = [operand2, '=', operand1]
                        self.IRS.append(ir)
                else:
                    # e,g : if we have +=, operator1 is '+', operator2 is '='
                    if (len(node.name) == 2):
                        operator1 = node.name[0]
                        operator2 = node.name[1]
                    # >>= and <<= , operator1 is '>>' or '<<', operator2 is '='
                    elif(len(node.name) == 3):
                        operator1 = node.name[0] + node.name[1]
                        operator2 = node.name[2]
                    operand1 = self.dequeue()
                    operand2 = self.dequeue()
                    ir = [operand2, operator2, operand2, operator1, operand1]
                    self.IRS.append(ir)
        return operand2

    # Translate expression without assignment into IR using temporary
    # variables (e.g. a >> 1, 1 + 2 + 3, etc.)
    # parameters: nodes, AST subtree with relevant parsed data
    def simpleExpr(self, nodes):
        subtree = self.getSubtree(nodes)
        operand2 = ''
        self.queue = []
        for node in reversed(subtree):
            if (node.name not in arithmetic):
                # Enqueue identifiers and constants
                self.enqueue(node.name)
            elif (node.name in arithmetic and node.name != '!' and len(node.children) != 1):
                # Handle binary operators
                operand2 = self.dequeue()
                operand1 = self.dequeue()
                operator = node.name
                tempVar = 't_' + str(self.temporaryVarible)
                ir = [tempVar, '=', operand1, operator, operand2]
                self.IRS.append(ir)
                self.enqueue(tempVar)
                self.temporaryVarible += 1
            elif (node.name == '!'):
                # Handle !
                operand1 = self.dequeue()
                operator = node.name
                self.enqueue(operator+operand1)
            elif(node.name == '-' and len(node.children) == 1):
                # Handle negative number
                operand1 = self.dequeue()
                operator = node.name
                self.enqueue(operator+operand1)
        self.dequeue()
        return tempVar
    
    # Translate variable declaration without assignment into IR
    # Not necessary for the final IR
    # parameters: nodes, AST subtree with relevant parsed data
    def varDecl(self, nodes):
        for node in nodes:
            if(node.name != None):
                self.IRS.append([node.name])
    
    # Translate goto statement into IR.
    # parameters: nodes, AST subtree with relevant parsed data
    def gotoStmt(self, nodes):
        for node in nodes.children:
            self.IRS.append(['goto', node.name])

    # Create a label for goto statements, conditionals, or loops
    # parameters: nodes, AST subtree with relevant parsed data
    # parameters: type, determines whether or not to return the label
    # to the caller
    # If: type is loop label or condition label, return the label to caller
    # instead of appending to IR
    # Else if: label name already exists, creates the label with available name
    # (e.g 'goto even:', 'label even:')
    def createLabel(self, nodes, type):
        if (type != None):
            loopL = 'L' + str(self.label) + ':'
            self.label += 1
            return loopL
        else:
            for node in nodes.children:
                self.IRS.append([node.name + ':'])
        
    # Translate return statement into IR
    # parameters: nodes, AST subtree with relevant parsed data
    def returnStmt(self, nodes):
        for node in nodes.children:
            if (node.name in assignment):
                # Handle assignments
                operand = self.assign(node)
                self.IRS.append(['ret', operand])
            elif (node.name in arithmetic):
                # Handle arithmetic expressions
                tempVar = self.simpleExpr(node)
                self.IRS.append(['ret', tempVar])
            elif ('func-' in str(node.name)):
                # Handle function calls
                self.funcCall(node, node.name, 1, 0)
            else:
                self.IRS.append(['ret', node.name])

    # Translates increment and decrement statements into IR
    def increment(self, nodes, name):
        operator = name[0]
        for node in nodes.children:
            self.IRS.append([node.name, '=', node.name, operator, '1'])

    # Translate function calls into IR
    # parameters: funcName, name of the function
    # parameters: nodes, AST subtree with relevant parsed data
    # parameters: retStmtFlag, indicates whether or not the call happens in a return statement
    # parameters: exprFlag, indicates whether or not to append to IR or return to caller
    # In normal case, it appends the func call to  IRS. e,g 'add(a , b)' will be append to the IRS
    # In special case such as func call in returnStmt, it appends 'ret add(a, b)'
    # and if funcCall is in expr, such as a * add(i, j). return the IR instead of appending to the IRS
    def funcCall(self, nodes, funcName, retStmtFlag, exprFlag):
        ir = []
        # Obtain the call arguments
        argsCount = self.args(nodes, funcName, 1)
        if(exprFlag):
            tempCount = argsCount
            while (tempCount > 0):
                self.dequeue()
                tempCount -= 1
        funcName = funcName.replace('func-', '')
        if(retStmtFlag):
            ir.append('ret ' + funcName + ' (')
        else:
            ir.append(funcName + ' (')
        while argsCount > 0:
            ir.append(str(self.dequeue()))
            if argsCount != 1:
                ir.append(',')
            argsCount -= 1
        ir.append(')')
        if(exprFlag):
            return ir
        else:
            self.IRS.append(ir)

    # Translate while loop into IR
    # parameters: nodes, AST subtree with relevant parsed data
    def whileloop(self, nodes):
        # Create labels for loop entry, condition, and end
        self.enterLoopLabel = self.createLabel(nodes, 'loop')
        self.loopConditionLabel = self.createLabel(nodes, 'condition')
        self.endLoopLabel = self.createLabel(nodes, 'loop')
        
        self.IRS.append(['goto', self.loopConditionLabel])
        self.IRS.append([self.enterLoopLabel])
        
        for node in nodes.children:
            if (node.name == 'stmt'):
                self.statement(node)
                
        self.IRS.append([self.loopConditionLabel])
        for node in nodes.children:
            if (node.name == 'condition'):
                self.loopConditions(node)
        self.IRS.append([self.endLoopLabel])

    # Translate do-while loop into IR
    # parameters: nodes, AST subtree with relevant parsed data
    # Note: Dowhile loop IR does not have the goto condition label before the stmt body. 
    # That is the only difference between while and dowhile
    def dowhile(self, nodes):
        # Create labels for loop entry, condition, and end
        self.enterLoopLabel = self.createLabel(nodes, 'loop')
        self.loopConditionLabel = self.createLabel(nodes, 'condition')
        self.endLoopLabel = self.createLabel(nodes, 'loop')
        
        self.IRS.append([self.enterLoopLabel])
       
        for node in nodes.children:
            if (node.name == 'stmt'):
                self.statement(node)
        
        self.IRS.append(['goto', self.loopConditionLabel])
        self.IRS.append([self.loopConditionLabel])
        for node in nodes.children:
            if (node.name == 'condition'):
                self.loopConditions(node)
        self.IRS.append([self.endLoopLabel])

    # Translate for loop into IR
    # parameters: nodes, AST subtree with relevant parsed data
    # This function places for loop labels at their correct positions and 
    # the condition and body conversion is done by calling other functions
    def forloop(self, nodes):
        # Create labels for loop entry, condition, and end
        self.enterLoopLabel = self.createLabel(nodes, 'loop')
        self.loopConditionLabel = self.createLabel(nodes, 'condition')
        self.endLoopLabel = self.createLabel(nodes, 'loop')
        
        for node in nodes.children:
            if (node.name == 'init'):
                for n in node.children:
                    if (n.name == '='):
                        self.assign(n)
                    else:
                        self.varDecl(n)
                        
        self.IRS.append(['goto', self.loopConditionLabel])
        self.IRS.append([self.enterLoopLabel])
        for node in nodes.children:
            if (node.name == 'stmt'):
                self.statement(node)
            elif (node.name == 'increment'):
                for n in node.children:
                    if (n.name == '++' or n.name == '--'):
                        self.increment(n, n.name)
                    elif (n.name in assignment):
                        self.assign(n)
                            
        self.IRS.append([self.loopConditionLabel])
        for node in nodes.children:
            if (node.name == 'condition'):
                self.loopConditions(node)
        self.IRS.append([self.endLoopLabel])

    # Translate break statement into IR
    # parameters: nodes, AST subtree with relevant parsed data
    # Break statement is replaced with a goto statement 
    # which goes to the loop exit label 
    def breakStmt(self, nodes):
        self.IRS.append(['goto', self.endLoopLabel])

    # Converting continue statement, 
    # continue statement is replace with goto statement 
    # which goes to the beginning of loop conditions label 
    def continueStmt(self, nodes):
        self.IRS.append(['goto', self.loopConditionLabel])

    # Converts loop conditional statement
    # the conditional statement can be boolean expression with only comparsion ops(simpleBool)
    # or boolean expression with logical ops (complexBool). 
    # in either case, corresponding function will be called.
    def loopConditions(self, nodes):
        for node in nodes.children:
            if (node.name == '&&' or node.name == '||'):
                res = node.to_array()
                booleanExpr = res['name']
                self.complexBool(booleanExpr)
                self.addBoolToIR()
            if (node.name in comparison):
                self.simpleBool(node)
    
    # Handles simple boolean expression in loop conditional statements
    # it analysis the flow of boolean expression and decide where to jump when expr is 
    # false or true. 
    def simpleBool(self, nodes):
        opand = []
        for node in nodes.children:
            if (node.name not in comparison and node.name != '!' and node.name not in arithmetic):
                opand.append(node.name)
            elif (node.name in arithmetic):
                temp = self.simpleExpr(node)
                opand.append(temp)
            elif (node.name == '!'):
                opand.append(node.name + str(node.children[0]).replace(';', '').strip())
        expr = opand[0] + nodes.name + opand[1]
        list = ['if', expr, 'goto', self.enterLoopLabel, 'else', 'goto', self.endLoopLabel]
        self.IRS.append(list)

    # ComplexBool function handles complex boolean expression in loop conditional statements
    # it parses the logic ops and converts the left and right hand side of logic ops. 
    # the function uses dictionary to store the label information so that expressions 
    # know where to jump when false or true. 
    def complexBool(self, booleanExpr):
        queue = []
        compareStack = []
        logicQueue = []
        EnOrder = {}
        order = 0
        jumpTrue = {}
        jumpFlase = {}
        i = 0
        for item in booleanExpr:
            if (item not in alc and item != '!'):
                queue.append(item)
            elif (item == '!'):
                op1 = queue.pop(0)
                queue.append(item + op1)
            elif (item in arithmetic):
                operand2 = queue.pop(0)
                operand1 = queue.pop(0)
                operator = item
                tempVar = 't_' + str(self.temporaryVarible)
                queue.append(tempVar)
            elif (item in comparison):
                op1 = queue.pop(0)
                op2 = queue.pop(0)
                relop = item
                if (i == 0):
                    label = self.loopConditionLabel
                    i += 1
                else:
                    label = self.createLabel(None, 'condition')
                expr = op1 + relop + op2
                dict = {expr : label}
                self.labelPlace.update(dict)
        queue = []
        for item in booleanExpr:
            if (item not in alc and item != '!'):
                queue.append(item)
            elif (item == '!'):
                op1 = queue.pop(0)
                queue.append(item + op1)
            elif (item in arithmetic):
                operand2 = queue.pop(0)
                operand1 = queue.pop(0)
                operator = item
                tempVar = 't_' + str(self.temporaryVarible)
                ir = [tempVar, '=', operand1, operator, operand2]
                self.IRS.append(ir)
                queue.append(tempVar)
                self.temporaryVarible += 1
            elif (item in comparison):
                op1 = queue.pop(0)
                op2 = queue.pop(0)
                relop = item
                expr =  str(op1) + relop + str(op2)
                dict = {expr : None}
                compareStack.append(expr)
                dict = {expr : order}
                EnOrder.update(dict)
            elif (item in logical):
                # expr && logicExpr
                # logicalExpr && expr
                if(len(compareStack) == 1):
                    expr1 = compareStack.pop()
                    expr2 = logicQueue.pop(0)
                    order1 = str(expr1).replace('[', '').replace(']', '').replace("'", '')
                    order2 = str(expr2).replace('[', '').replace(']', '').replace("'", '')
                    order1 = int(EnOrder[order1])
                    order2 = int(EnOrder[order2])
                    logic = item
                    if(order1 < order2): 
                        expr2_1 = self.getSubExpr(expr2, 'LHS')
                        expr = str(expr1) + logic + str(expr2)
                        logicQueue.append([expr])
                        dict = {expr : order}
                        EnOrder.update(dict)
                        self.placeLabel(str(expr1), expr2_1, logic, 2)
                    else:
                        expr2_1 = self.getSubExpr(expr2, 'LHS')
                        expr2_2 = self.getSubExpr(expr2, 'RHS')
                        expr = str(expr2) + logic + str(expr1)
                        logicQueue.append([expr])
                        dict = {expr : order}
                        EnOrder.update(dict)
                        self.placeLabel([expr2_1, expr2_2], expr1, logic, 4)
                # logicalExpr && logicalExpr
                elif (len(logicQueue) == 2):
                    expr2 = logicQueue.pop(0)
                    expr1 = logicQueue.pop(0)
                    expr1_1 = self.getSubExpr(expr1, 'LHS')
                    expr1_2 = self.getSubExpr(expr1, 'RHS')
                    expr2_1 = self.getSubExpr(expr2, 'LHS')
                    logic = item
                    expr = str(expr1) + logic + str(expr2)
                    logicQueue.append([expr])
                    self.placeLabel([expr1_1, expr1_2], expr2_1, logic, 3)
                    dict = {expr : order}
                    EnOrder.update(dict)
                # expr1 && expr2 
                else :
                    expr2 = compareStack.pop()
                    expr1 = compareStack.pop()
                    logic = item
                    expr = str(expr1) + logic + str(expr2)
                    logicQueue.append([expr])
                    dict = {expr : order}
                    EnOrder.update(dict)
                    self.placeLabel(str(expr1), str(expr2), logic, 1)
            order += 1
    
    
    # The function decides where to place the label for the given 
    # expressions. It handels different cases that a boolean expression
    # with logic ops can be. The self.labelPlace will store the 
    # updated label location. 
    def placeLabel(self, expr1, expr2, logic, flag):
        if (logic == '&&' and flag == 1):
            place = self.labelPlace[expr1]
            place2 = self.labelPlace[expr2]
            placeIFtrue = self.enterLoopLabel
            placeIFfalse = self.endLoopLabel
            dic = [place, placeIFtrue, placeIFfalse]
            self.labelPlace[expr1] = dic
            dic = [place2, placeIFtrue, placeIFfalse]
            self.labelPlace[expr2] = dic

        elif (logic == '||' and flag == 1):
            place = self.labelPlace[expr1]
            placeIFtrue = self.enterLoopLabel
            placeIFfalse = str(self.labelPlace[expr2])
            dic = [place, placeIFtrue, placeIFfalse]
            self.labelPlace[expr1] = dic

            place = self.labelPlace[expr2]
            placeIFtrue = self.enterLoopLabel
            placeIFfalse = self.endLoopLabel
            dic = [place, placeIFtrue, placeIFfalse]
            self.labelPlace[expr2] = dic

        elif (logic == '||' and flag == 2 ):
            placeExpr1 = self.labelPlace[expr1]
            placeIFtrue = self.enterLoopLabel
            placeIFfalse = self.labelPlace[expr2][0]
            dic = [placeExpr1, placeIFtrue, placeIFfalse]
            self.labelPlace[expr1] = dic

        elif (logic == '&&' and flag == 2 ):
            placeExpr1 = self.labelPlace[expr1]
            placeIFtrue = self.labelPlace[expr2][0]
            placeIFfalse = self.endLoopLabel
            dic = [placeExpr1, placeIFtrue, placeIFfalse]
            self.labelPlace[expr1] = dic
        
        elif (logic == '&&' and (flag == 3 or flag == 4)):
            if (flag == 4):
                placeExpr2_1 = self.labelPlace[expr2]
            else:
                placeExpr2_1 = self.labelPlace[expr2][0]

            placeExpr1_1 = self.labelPlace[expr1[0]]
            placeExpr1_2 = self.labelPlace[expr1[1]]
            newLabel = []
            for labels in placeExpr1_1: 
                if (self.enterLoopLabel == labels):
                    newLabel.append(placeExpr2_1)
                else :
                    newLabel.append(labels)
            self.labelPlace[expr1[0]] = newLabel

            newLabel = []
            for labels in placeExpr1_2: 
                if (self.enterLoopLabel == labels):
                    newLabel.append(placeExpr2_1)
                else :
                    newLabel.append(labels)
            self.labelPlace[expr1[1]] = newLabel
            if (flag == 4):
                newLabel = [placeExpr2_1, self.enterLoopLabel, self.endLoopLabel]
                self.labelPlace[expr2] = newLabel

        elif (logic == '||' and (flag == 3 or flag == 4)):
            if (flag == 4):
                placeExpr2_1 = self.labelPlace[expr2]
            else:
                placeExpr2_1 = self.labelPlace[expr2][0]
        
            placeExpr1_1 = self.labelPlace[expr1[0]]
            placeExpr1_2 = self.labelPlace[expr1[1]]

            newLabel = []
            for labels in placeExpr1_1: 
                if (self.endLoopLabel == labels):
                    newLabel.append(placeExpr2_1)
                else :
                    newLabel.append(labels)
            self.labelPlace[expr1[0]] = newLabel
            newLabel = []
            for labels in placeExpr1_2: 
                if (self.endLoopLabel == labels):
                    newLabel.append(placeExpr2_1)
                else :
                    newLabel.append(labels)
            self.labelPlace[expr1[1]] = newLabel
            if (flag == 4):
                newLabel = [placeExpr2_1, self.enterLoopLabel, self.endLoopLabel]
                self.labelPlace[expr2] = newLabel

    # ifStmt function creates the inital labels for if statement 
    # store the label for 'if', 'else if', and 'else' nodes
    # those labels are important for deciding the jump location 
    def ifstmt(self, nodes):
        self.ifLabel = []
        self.elifLabel = []
        self.elseLabel = []
        self.conditionLabel = []
        
        for node in nodes.children:
            if (node.name == 'if'):
                label = self.createLabel(None, 'condiiton')
                list = [label, node]
                self.ifLabel.append(list)

            elif (node.name == 'elseif'):
                label = self.createLabel(None, 'condiiton')
                list = [label, node]
                self.elifLabel.append(list)

            elif (node.name == 'else'):
                label = self.createLabel(None, 'condiiton')
                list = [label, node]
                self.elseLabel.append(list)

        for node in nodes.children:
                condLabel = self.createLabel(None, 'condiiton')
                self.conditionLabel.append(condLabel)

        self.exitIFLabel = self.createLabel(None, 'condiiton')
        list = ['goto', self.conditionLabel[0]]
        self.IRS.append(list)

        enterLabel = self.ifLabel[0][0]
        self.enterIFlabel = enterLabel
        self.IRS.append([enterLabel])
        self.placeStmt(self.ifLabel[0][1])
        
        if(len(self.elifLabel) != 0):
            for label in self.elifLabel:
                self.IRS.append([label[0]])
                self.placeStmt(label[1])
        if(len(self.elseLabel) != 0):
            for label in self.elseLabel:
                self.IRS.append([label[0]])
                self.placeStmt(label[1])
                list = ['goto', self.exitIFLabel]   
                self.IRS.append(list)
        i = 0
        for node in nodes.children:
            if (node.name != 'else'):
                for n in node.children:
                    if(n.name == 'condition'):
                        self.IRS.append([self.conditionLabel[i]])
                        self.ifConditional(n, i, node.name)
            else:
                self.IRS.append([self.conditionLabel[i]])
                gotoTrue = str(self.elseLabel[0][0])
                list = ['goto', gotoTrue]   
                self.IRS.append(list)
            i += 1    
        self.IRS.append([self.exitIFLabel])   

    # The function scanns the if statement nodes, and recognizes the boolean expression 
    # in the if conditionals. when no logic ops are in side the conditionals, the function
    # passes node to simpleIF function.  
    def ifConditional(self, nodes, order, parent):
        for node in nodes.children:
            if(node.name in comparison):
                self.simpleIF(node,order, parent)
            elif(node.name in logical):
                self.complexIF(node,order, parent)
    
    # The function converts IF statement with simple boolean expression 
    # which means the boolean expresion only contains comparsion ops, 
    # logical ops can not be converted. 
    def simpleIF(self, nodes,order, parent):
        opand = []
        list = []
        for node in nodes.children:
            if (node.name not in comparison and node.name != '!' and node.name not in arithmetic):
                opand.append(node.name)
            elif (node.name in arithmetic):
                temp = self.simpleExpr(node)
                opand.append(temp)
            elif (node.name == '!'):
                opand.append(node.name + str(node.children[0]).replace(';', '').strip())
            print(opand)
        expr = opand[0] + nodes.name + opand[1]

        if (parent == 'if'):
            gotoTrue = str(self.ifLabel[0][0])
            if (len(self.conditionLabel) > 1):
                gotoFalse = self.conditionLabel[order + 1]
            else :
                gotoFalse = self.exitIFLabel
            list = ['if', expr, 'goto', gotoTrue, 'else', 'goto', gotoFalse]

        elif (parent == 'elseif'):
            gotoTrue = str(self.elifLabel[order-1][0])
            if(order + 1 < len(self.conditionLabel)):
                gotoFalse = self.conditionLabel[order + 1]
            else:
                gotoFalse = self.exitIFLabel
            list = ['if', expr, 'goto', gotoTrue, 'else', 'goto', gotoFalse]   
        self.IRS.append(list)


    def complexIF(self, nodes, order, parent):
        pass
    
    # helper function that breaks down the given expr 
    # the give expr should be boolean expression with logical ops
    # the function returns left hand side or right hand side of the expr 
    def getSubExpr(self, expr, flag):
        expr = str(expr)
        result = ''
        if ('||' in expr):
            temp = expr.split('||')
        elif ('&&' in expr):
            temp = expr.split('&&')
        
        if (flag == 'LHS'):
            temp[0] = temp[0].replace('[', '')
            temp[0] = temp[0].replace("'", '')
            temp[0] = temp[0].strip()
            result = temp[0]
        
        elif (flag == 'RHS'):
            temp[1] = temp[1].replace(']', '')
            temp[1] = temp[1].replace("'", '')
            temp[1] = temp[1].strip()
            result = temp[1]
        return result
        
    # Helper function that calls statement function and pass the node
    # The purpose is to reduce the function size of the caller. 
    def placeStmt(self, nodes):
        for node in nodes.children:
                if (node.name == 'stmt'):
                    self.statement(node)

    # Helper function that read label from self.labelPlace 
    # and place the label with expression
    def addBoolToIR(self):
        i = 0
        for expr in self.labelPlace:
            if (i == 0):
                labelPlace = self.loopConditionLabel
                i += 1
            else:
                labelPlace = self.labelPlace[expr][0]
                self.IRS.append([labelPlace])
            labelIFtrue = self.labelPlace[expr][1]
            labelIFfalse = self.labelPlace[expr][2]
            list = ['if', expr, 'goto', labelIFtrue, 'else', 'goto', labelIFfalse]
            self.IRS.append(list)

    # The function returns the subtree of given node
    def getSubtree(self, nodes):
        subtree = []
        for node in nodes.levelorder():
            subtree.append(node)
        return subtree

    # insert the item into the queue
    def enqueue(self, item):
        self.queue.append(item)

    # pop the item from the queue
    def dequeue(self):
        return self.queue.pop(0)

    # Perform simple calculation on the two given operands
    def simpleArithmetic(self, opnd1, oprt, opnd2):
        result = 0 
        if (oprt == '+'):
            result = opnd1 + opnd2
        elif (oprt == '-'):
            result = opnd1 - opnd2
        elif (oprt == '*'):
            result = opnd1 * opnd2
        elif (oprt == '/'):
            result = opnd1 / opnd2
        elif (oprt == '%'):
            result = opnd1 % opnd2
        elif (oprt == '|'):
            result = opnd1 | opnd2
        elif (oprt == '&'):
            result = opnd1 & opnd2
        elif (oprt == '^'):
            result = opnd1 ^ opnd2
        elif (oprt == '<<'):
            result = opnd1 << opnd2
        elif (oprt == '>>'):
            result = opnd1 >> opnd2
        return result

    def printIR(self):
        str1 = " "
        indentFlag = 0
        for list in self.IRS:
            if (str1.join(list) == '{'):
                indentFlag = 1
                print(str1.join(list))
                continue
            elif (str1.join(list) == '}'):
                indentFlag = 0
                print(str1.join(list))
                continue
            elif (indentFlag):
                print('\t', str1.join(list))
            else:
                print(str1.join(list))

    # Read the IR from fileString into the IR structure
    def readIR(self, fileString):
        fileString = [x.strip() for x in fileString]  
        fileString = [x.replace('\t', ' ') for x in fileString]  
        for line in fileString:
            list = line.split()
            self.IRS.append(list)
    