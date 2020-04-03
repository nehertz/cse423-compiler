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
        if (ast != None):
            self.treeString = ast
            self.tree = TreeNode.read(StringIO(ast))
        self.temporaryVarible = 0
        self.label = 0

        # LL stands for Loop Label
        self.LL = 0

        # CL Stands for condition label
        self.CL = 0

    def run(self):

        # TODO: change to levelorder, and only use the first level.
        for node in self.tree.children:
            # handle function name node
            if ('func-' in str(node.name)):
                self.funcNode(node, node.name)

            # handle global varible declration without assigment
            elif (node.name == 'varDecl'):
                self.varDecl(node)
            # handle global varible declration with assigment
            elif (node.name in assignment):
                self.assign(node)

        return self.IRS

    def funcNode(self, nodes, funcName):
        funcName = funcName.replace('func-', '')
        for node in nodes.children:
            if (node.name == 'args'):
                self.args(node, funcName, None)
            if (node.name == 'stmt'):
                self.statement(node)
        self.IRS.append(['}'])

    # The funcCallFlag is used to handle function call args
    # if funcCallFlag = 1，the args is from function call instead of function defination
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

    # TODO: Add option for printing to IR; add return values to return a list of statements
    def statement(self, nodes, addToIR=True):
        statements = []

        for node in nodes.children:
            # convert var decl with assignment
            # int a = expr or a = expr
            if (node.name in assignment):
                if addToIR:
                    self.assign(node, addToIR)
                else:
                    statements.append(self.assign(node, addToIR))

            # convert the var-decl without assignment
            # Example: int a 
            elif (node.name == 'varDecl'):
                if addToIR:
                    self.varDecl(node, addToIR)
                else:
                    statements.append(self.varDecl(node, addToIR))

            # convert function calls.
            elif ('func-' in str(node.name)):
                if addToIR:
                    self.funcCall(node, node.name, 0, 0)
                else:
                    statements.append(self.funcCall(node, node.name, 0, 1))

            elif(node.name == 'condStmt'):
                # Handle conditional statments
                if addToIR:
                    self.condStmt(node, addToIR)
                else:
                    statements.append(self.condStmt(node, addToIR))

            # convert simple expressions
            # those are expressions without assignment
            # examples : '1 + 2 + 3', 'a << 1'
            # reference to scanner for the alc list,
            elif (node.name in alc):
                if addToIR:
                    self.simpleExpr(node, addToIR)
                else:
                    statements.append(self.simpleExpr(node, addToIR))

            # convert the goto stmt, and its label
            elif (node.name == 'goto'):
                if addToIR:
                    self.gotoStmt(node, addToIR)
                else:
                    statements.append(self.gotoStmt(node, addToIR))

            elif (node.name == 'label'):
                if addToIR:
                    self.createLabel(node, None, addToIR)
                else:
                    statements.append(self.createLabel(node, None, addToIR))

            # convert return stmt
            elif (node.name == 'return'):
                if addToIR:
                    self.returnStmt(node, addToIR)
                else:
                    statements.append(self.returnStmt(node, addToIR))

            # convert increment and decrement, ++a and --a
            # the a = ++a case is handled by the assign() function
            elif (node.name == '++' or node.name == '--'):
                if addToIR:
                    self.increment(node, node.name, addToIR)
                else:
                    statements.append(self.increment(node, node.name, addToIR))

            # convert while loop
            elif (node.name == 'while'):
                if addToIR:
                    self.whileloop(node, addToIR)
                else:
                    statements.append(self.whileloop(node, addToIR))

            elif (node.name == 'dowhile'):
                if addToIR:
                    self.dowhile(node, addToIR)
                else:
                    statements.append(self.dowhile(node, addToIR))

            elif (node.name == 'forLoop'):
                if addToIR:
                    self.forloop(node, addToIR)
                else:
                    statements.append(self.forloop(node, addToIR))

        if not addToIR:
            return statements

    def assign(self, nodes, addToIR=True):
        subtree = self.getSubtree(nodes)
        operand2 = ''
        self.queue = []
        statements = []
        for node in reversed(subtree):
            # print(self.queue)
            # print(node.name)
            if(node.name not in operators.keys() and 'func' not in node.name and node.name != 'args' and node.name != 'cast'):
                self.enqueue(node.name)
            elif(node.name not in assignment and node.name in alc):
                operand2 = self.dequeue()
                operand1 = self.dequeue()
                operator = node.name
                tempVar = 't_' + str(self.temporaryVarible)
                self.temporaryVarible += 1
                ir = [tempVar, '=', operand1, operator, operand2]
                if addToIR:
                    self.IRS.append(ir)
                else:
                    statements.append(ir)
                self.enqueue(tempVar)
            elif(node.name == '++' or node.name == '--'):
                operand1 = self.dequeue()
                operator = node.name[0]
                ir = [operand1, '=', operand1, operator, '1']
                if addToIR:
                    self.IRS.append(ir)
                else:
                    statements.append(ir)
                self.enqueue(operand1)
            elif('func' in node.name):
                ir = " ".join(self.funcCall(node, node.name, 0, 1))
                tempVar = 't_' + str(self.temporaryVarible)
                self.temporaryVarible += 1
                ir = [tempVar, '=', ir]
                if addToIR:
                    self.IRS.append(ir)
                else:
                    statements.append(ir)
                self.enqueue(tempVar)
            elif(node.name == 'cast'):
                operand = self.dequeue() 
                typeSpec = self.dequeue()
                ir = '(' + str(typeSpec) + ')' +  str(operand)
                self.enqueue(ir)
            elif(node.name in assignment):
                if(node.name == '='):
                    operand1 = self.dequeue()
                    operand2 = self.dequeue()
                    ir = [operand2, '=', operand1]
                    if addToIR:
                        self.IRS.append(ir)
                    else:
                        statements.append(ir)
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
                    if addToIR:
                        self.IRS.append(ir)
                    else:
                        statements.append(ir)

        if addToIR:
            return operand2
        else:
            return statements

    # simpleExpr converts experssion which does not have assigment
    # updated 3/30/20: now supports logical and comparison ops and unary ops
    # e,g a >> 1, 1 + 2 + 3
    def simpleExpr(self, nodes, addToIR=True):
        subtree = self.getSubtree(nodes)
        ops = alc
        unary = ['~', '!']
        operand2 = ''
        statements = []
        self.queue = []
        for node in reversed(subtree):
            if (node.name not in ops):
                self.enqueue(node.name)
            elif (node.name in ops):
                if (node.name in unary):
                    operand1 = self.dequeue()
                    operator = node.name
                    tempVar = 't_' + str(self.temporaryVarible)
                    ir = [tempVar, '=', operator + operand1]
                else:
                    operand2 = self.dequeue()
                    operand1 = self.dequeue()
                    operator = node.name
                    tempVar = 't_' + str(self.temporaryVarible)
                    ir = [tempVar, '=', operand1, operator, operand2]

                if addToIR:
                    self.IRS.append(ir)
                else:
                    statements.append(ir)
                self.enqueue(tempVar)
                self.temporaryVarible += 1
        self.dequeue()
        if addToIR:
            return tempVar
        else:
            return statements

    def varDecl(self, nodes, addToIR=True):
        for node in nodes:
            if(node.name != None):
                if addToIR:
                    self.IRS.append(node.name)
                else:
                    return node.name

    # TODO: need to have our own goto rules.
    def gotoStmt(self, nodes, addToIR=True):
        for node in nodes.children:
            if addToIR:
                self.IRS.append(['goto', node.name])
            else:
                return ['goto', node.name]

    # creates label for goto stmt and loops
    # if type is loopLabel,
    # use the loopLabel global varible to create the label
    # else if the label name is already exist, for example in goto stmt,
    # 'goto even:'
    # 'lable even:'
    # then creates the label 'even'
    def createLabel(self, nodes, type, addToIR=True):
        if (type == 'loop'):
            loopL = 'LL' + str(self.LL) + ':'
            # self.IRS.append(loopL)
            self.LL += 1
            return loopL
        elif (type == 'condition'):
            loopL = 'CL' + str(self.CL) + ':'
            self.CL += 1
            return loopL
        else:
            for node in nodes.children:
                if addToIR:
                    self.IRS.append([node.name, ':'])
                else:
                    return [node.name, ':']

    # Samll helper function to create 'goto label:'
    # example: if label = 'loop1'
    # the function will append 'goto loop1' to the IRS
    def createGotoLabel(self, label):
        self.IRS.append(['goto', label])

    # return statement support var assign and func calls
    # return 1; return b;
    # return 1+2;
    # return a = 1 + 2;
    # return add();
    def returnStmt(self, nodes, addToIR=True):
        for node in nodes.children:
            if (node.name in assignment):
                operand = self.assign(node)
                if addToIR:
                    self.IRS.append(['ret', operand])
                else:
                    return ['ret', operand]
            elif (node.name in arithmetic):
                tempVar = self.simpleExpr(node)
                if addToIR:
                    self.IRS.append(['ret', tempVar])
                else:
                    return ['ret', tempVar]
            elif ('func-' in str(node.name)):
                # Treating funcCall a bit different since there was already a method for returning the expr using exprFlag
                if addToIR:
                    self.funcCall(node, node.name, 1, 0)
                else:
                    return self.funcCall(node, node.name, 1, 1)
            else:
                if addToIR:
                    self.IRS.append(['ret', node.name])
                else:
                    return ['ret', node.name]

    # the increment function inputs '++' or '--' node and name of the node
    # convert a++ to a = a + 1, and append it to the IRS
    def increment(self, nodes, name, addToIR=True):
        operator = name[0]
        for node in nodes.children:
            if addToIR:
                self.IRS.append([node.name, '=', node.name, operator, '1'])
            else:
                return [node.name, '=', node.name, operator, '1']

    # funcCall function calls the args function to obtain the call arguments
    # In normal case, it appends the func call to  IRS. e,g 'add(a , b)' will be append to the IRS
    # In special case such as func call in returnStmt, it appends 'ret add(a, b)'
    # and if funcCall is in expr, such as a * add(i, j). return the IR instead of appending to the IRS
    def funcCall(self, nodes, funcName, retStmtFlag, exprFlag):
        ir = []
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

    def condParse(self, stmt):
        # Parse an complex expression and break it down to
        # E1 && E2
        # E1 || E2
        # !E
        # (E)
        subtree = self.getSubtree(stmt)
        ops = arithmetic + comparison
        unary = ['~', '!']
        operand2 = ''
        # tempVar = ''
        # expr = []
        self.queue = []
        for node in reversed(subtree):
            if (node.name in logical):
                # self.enqueue(node.name)
                if (node.name == '!'):
                    expr = [node.name, self.dequeue()]
                    self.enqueue(expr)
                else:
                    expr = [node.name, [self.dequeue(), self.dequeue()]]
                    self.enqueue(expr)
            elif (node.name not in ops):
                self.enqueue(node.name)
            elif (node.name in ops):
                if (node.name in unary):
                    operand1 = self.dequeue()
                    operator = node.name
                    # tempVar = 't_' + str(self.temporaryVarible)
                    # ir = [tempVar, '=', operator + operand1]
                    self.enqueue(operator + operand1)
                else:
                    operand2 = self.dequeue()
                    operand1 = self.dequeue()
                    operator = node.name
                    # tempVar = 't_' + str(self.temporaryVarible)
                    # ir = [tempVar, '=', operand1, operator, operand2]
                    self.enqueue(operand1 + ' ' + operator + ' ' + operand2)
                # self.IRS.append(ir)
                # self.enqueue(tempVar)
                # self.temporaryVarible += 1
            # print(self.queue)
            
        self.dequeue()
        return expr

    # TODO: Add comments
    # TODO: Add toggling for adding to IR after implementing adding to IR
    def condStmt(self, nodes, addToIR=True):
        conds = {}
        # conds format: conds[<if+if#/else>] = [<if-condition>, <if-block>, <if-label>]
        ifCount = 0
        bCount = 0

        for i, stmt in enumerate(nodes):
            # Collect conditional statement info
            if (stmt.name == 'if' or stmt.name == 'else-if'):
                # Handle if and else if
                cond = self.condParse(stmt[0])
                # cond.reverse()

                # self.IRS.append([stmt.name + ' (' + str(cond) + ')'])
                # self.IRS.append(['{'])
                # self.statement(stmt.children[1])
                # self.IRS.append(['}'])

                if (i == 0):
                    # First if statement does not have a label
                    conds['block' + str(bCount)] = [self.statement(stmt.children[1], False), 'l_' + str(self.label)]
                    bCount += 1
                    self.label += 1
                    conds['if' + str(ifCount)] = [cond, None]
                else:
                    conds['if' + str(ifCount)] = [cond, self.statement(stmt.children[1], False), 'l_' + str(self.label)]
                    self.label += 1
                ifCount += 1
            else:
                # Handle else
                # self.IRS.append([stmt.name])
                # self.IRS.append(['{'])
                # self.statement(stmt.children[0])
                # self.IRS.append(['}'])
                conds['else'] = [None, self.statement(stmt.children[0], False), 'l_' + str(self.label)]
                self.label += 1

        # for cond in conds:
            # Generate conditional IR

            
        [print(k, v) for k, v in conds.items()]

    def whileloop(self, nodes, addToIR=True):
        enterLoopLabel = self.createLabel(nodes, 'loop')
        endLoopLable = self.createLabel(nodes, 'loop')
        # loopConditionLabel = self.createLabel(nodes, 'condition')

        # gotoLabel = self.createGotoLabel(loopConditionLabel)
        self.IRS.append([enterLoopLabel])
        self.IRS.append(['('])

        for node in nodes.children:
            if (node.name == 'stmt'):
                self.statement(node, addToIR)

        self.IRS.append([')'])

        # self.IRS.append([loopConditionLabel])
        for node in nodes.children:
            if (node.name == 'condition'):
                pass
                # self.loopConditions(node, enterLoopLabel, endLoopLable)
        self.IRS.append([endLoopLable])

    # Note: Dowhile loop IR does not have the goto condition label before the stmt body. 
    # That is the only difference between while and dowhile
    def dowhile(self, nodes, addToIR=True):
        enterLoopLabel = self.createLabel(nodes, 'loop')
        endLoopLable = self.createLabel(nodes, 'loop')
        self.IRS.append([enterLoopLabel])
        self.IRS.append(['('])

        for node in nodes.children:
            if (node.name == 'stmt'):
                self.statement(node)

        self.IRS.append([')'])

        # self.IRS.append([loopConditionLabel])
        for node in nodes.children:
            if (node.name == 'condition'):
                pass
                # self.loopConditions(node, enterLoopLabel, endLoopLable)
        self.IRS.append([endLoopLable])

    def forloop(self, nodes, addToIR=True):
        enterLoopLabel = self.createLabel(nodes, 'loop')
        endLoopLable = self.createLabel(nodes, 'loop')
        for node in nodes.children:
            if (node.name == 'init'):
                for n in node.children:
                    if (n.name == '='):
                        self.assign(n)
                    else:
                        self.varDecl(n)

        self.IRS.append([enterLoopLabel])
        self.IRS.append(['('])
        for node in nodes.children:
            if (node.name == 'stmt'):
                self.statement(node)
            elif (node.name == 'increment'):
                for n in node.children:
                    if (n.name == '++' or n.name == '--'):
                        self.increment(n, n.name)
                    elif (n.name in assignment):
                        self.assign(n)
        self.IRS.append([')'])

        for node in nodes.children:
            if (node.name == 'condition'):
                pass
        self.IRS.append([endLoopLable])

    # def loopConditions(self, nodes, enterLoopLabel, endLoopLable):
    #     for node in nodes.children:
    #         # && and ||, this means the conditions stmt is
    #         # composed by multiple conditions expression
    #         # for example, a > b && b > c
    #         if(node.name in logical):
    #             if (node.name == '&&'):
    #                 pass
    #             elif (node.name == '||'):
    #                 pass
    #         # >, < , != etc, this means the condition stmt only
    #         # has one condition expression
    #         # TODO: need discussion
    #         elif (node.name in comparison):
    #             subtree = self.getSubtree(node)
    #             operand2 = ''
    #             for n in reversed(subtree):
    #                 if (n.name not in comparison):
    #                     self.enqueue(n.name)
    #                 elif (n.name in comparison):
    #                     pass

    #         # the condition is arithmetric express
    #         # example: while(1 + 2)
    #         elif (node.name in arithmetic):
    #             tempVar = self.simpleExpr(node)
    #             ir = ['if', '(', str(tempVar), '!=', '0', ')',
    #                   'goto', enterLoopLabel]
    #             self.IRS.append(ir)
    #             ir = ['else', 'goto', endLoopLable]
    #             self.IRS.append(ir)
    #             self.enqueue(operand1)

    #         elif(node.name in assignment):
    #             if(node.name == '='):
    #                 operand1 = self.dequeue()
    #                 operand2 = self.dequeue()
    #                 ir = [operand2, '=', operand1]
    #                 self.IRS.append(ir)
    #             else:
    #                 # e,g : if we have +=, operator1 is '+', operator2 is '='
    #                 if (len(node.name) == 2):
    #                     operator1 = node.name[0]
    #                     operator2 = node.name[1]
    #                 # >>= and <<=
    #                 elif(len(node.name) == 3):
    #                     operator1 = node.name[0] + node.name[1]
    #                     operator2 = node.name[2]
    #                 operand1 = self.dequeue()
    #                 operand2 = self.dequeue()
    #                 ir = [operand2, operator2, operand2, operator1, operand1]
    #                 self.IRS.append(ir)
    #     return operand2

    def getSubtree(self, nodes):
        subtree = []
        for node in nodes.levelorder():
            subtree.append(node)
        return subtree

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.pop(0)

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

    def readIR(self, fileString):
        fileString = [x.strip() for x in fileString]  
        fileString = [x.replace('\t', ' ') for x in fileString]  
        for line in fileString:
            list = line.split()
            self.IRS.append(list)