from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_scanner import assignment
from ply_scanner import operators
from ply_scanner import arithmetic


class IR:
    def __init__(self, ast):
        self.IRS = []
        self.queue = []
        self.treeString = ast
        self.tree = TreeNode.read(StringIO(ast))
        self.temporaryVarible = 0

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

    def statement(self, nodes):
        for node in nodes.children:
            print("in stmt: " + node.name)
            # in statement block, handle var decl with assignment
            # note: only handles:
            # int a = expr or a = expr, since the root used to distinguish the node is assignment operator
            if (node.name in assignment):
                self.assign(node)
            # converting the var-decl without assignment
            elif (node.name == 'varDecl'):
                self.varDecl(node)
            # coverting conditional stmt
            elif (node.name == 'condStmt'):
                self.condStmt(node)
            # converting return stmt
            elif (node.name == 'return'):
                self.returnStmt(node)
            # converting increment and decrement, ++a and --a
            # the a = ++a case is handled by the assign() function
            elif (node.name == '++' or node.name == '--'):
                self.increment(node, node.name)
            # converting function calls.
            elif ('func-' in str(node.name)):
                self.funcCall(node, node.name, 0)

    def assign(self, nodes):
        subtree = self.getSubtree(nodes)
        operand2 = ''
        for node in reversed(subtree):
            if(node.name not in operators.keys()):
                self.enqueue(node.name)
            elif(node.name not in assignment and node.name in arithmetic):
                operand2 = self.dequeue()
                operand1 = self.dequeue()
                operator = node.name
                tempVar = 't_' + str(self.temporaryVarible)
                ir = [tempVar, '=', operand1, operator, operand2]
                self.IRS.append(ir)
                self.enqueue(tempVar)
                self.temporaryVarible += 1
            elif(node.name == '++' or node.name == '--'):
                operand1 = self.dequeue()
                operator = node.name[0]
                ir = [operand1, '=', operand1, operator, '1']
                self.IRS.append(ir)
                self.enqueue(operand1)

            elif(node.name in assignment):
                if(node.name == '='):
                    operand1 = self.dequeue()
                    operand2 = self.dequeue()
                    ir = [operand2, '=', operand1]
                    self.IRS.append(ir)
                else:
                    # e,g : if we have +=, operator1 is '+', operator2 is '='
                    if (len(node.name) == 2):
                        operator1 = node.name[0]
                        operator2 = node.name[1]
                    # >>= and <<=
                    elif(len(node.name) == 3):
                        operator1 = node.name[0] + node.name[1]
                        operator2 = node.name[2]
                    operand1 = self.dequeue()
                    operand2 = self.dequeue()
                    ir = [operand2, operator2, operand2, operator1, operand1]
                    self.IRS.append(ir)
        return operand2

    # simpleExpr converts experssion which does not have assigment
    # e,g a >> 1, 1 + 2 + 3
    # def simpleExpr(self, nodes):
    #     subtree = self.getSubtree(nodes)
    #     operand2 = ''
    #     for node in reversed(subtree):
    #         if (node.name not in alc):
    #             self.enqueue(node.name)
    #         elif (node.name in alc):
    #             operand2 = self.dequeue()
    #             operand1 = self.dequeue()
    #             operator = node.name
    #             tempVar = 't_' + str(self.temporaryVarible)
    #             ir = [tempVar, '=', operand1, operator, operand2]
    #             self.IRS.append(ir)
    #             self.enqueue(tempVar)
    #             self.temporaryVarible += 1
    #     self.dequeue()
    #     return tempVar

    def varDecl(self, nodes):
        for node in nodes:
            if(node.name != None):
                self.IRS.append([node.name])

    # TODO: Add comments
    # TODO: Check condition and create conditions with correct layout
    # TODO: Try and make the generation function usable for conditionals and loops alike
    # TODO: Short-circuiting
    def condStmt(self, nodes):
        for node in nodes.children:
            if (node.name == 'if' or node.name == 'else-if'):
                # Handle if and else if
                self.IRS.append([node.name + ':'])
                # self.statement(node.children[0])
                # FIXME: Need Andy's simpleExpr() function for arithmetic expressions
                self.statement(node.children[1])
            else:
                # Handle else
                self.IRS.append([node.name + ':'])
                self.statement(node.children[0])

    # return statement support var assign and func calls
    # return 1; return b;
    # return 1+2;
    # return a = 1 + 2;
    # return add();
    def returnStmt(self, nodes):
        for node in nodes.children:
            if (node.name in assignment):
                operand = self.assign(node)
                self.IRS.append(['ret', operand])
            elif ('func-' in str(node.name)):
                self.funcCall(node, node.name, 1)
            # TODO: simple experssions like 1+2+3
            else:
                self.IRS.append(['ret', node.name])

    # the increment function inputs '++' or '--' node and name of the node
    # convert a++ to a = a + 1, and append it to the IRS
    def increment(self, nodes, name):
        operator = name[0]
        for node in nodes.children:
            self.IRS.append([node.name, '=', node.name, operator, '1'])

    # funcCall function calls the args function to obtain the call arguments
    # In normal case, it appends the func call to  IRS. e,g 'add(a , b)' will be append to the IRS
    # In special case such as func call in returnStmt, it appends 'ret add(a, b)'

    def funcCall(self, nodes, funcName, retStmtFlag):
        ir = []
        argsCount = self.args(nodes, funcName, 1)
        #print("count  = ", argsCount)
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
        self.IRS.append(ir)

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
