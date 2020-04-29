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
        self.instr = 100
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
    def statement(self, nodes, addToIR=True):
        statements = []

        for node in nodes.children:
            # convert var decl with assignment
            # int a = expr or a = expr
            if (node.name in assignment):
                if addToIR:
                    self.assign(node, addToIR)
                else:
                    [statements.append(stmt) for stmt in self.assign(node, addToIR)]

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

            elif ('enum-' in str(node.name)):
                self.enumInst(node, node.name)

            elif(node.name == 'condStmt'):
                # Handle conditional statments
                if addToIR:
                    self.condStmt(node, addToIR)
                else:
                    # TODO: This might need to be changed to match others
                    statements.append(self.condStmt(node, addToIR))

            # convert simple expressions
            # those are expressions without assignment
            # examples : '1 + 2 + 3', 'a << 1'
            # reference to scanner for the alc list,
            elif (node.name in alc):
                if addToIR:
                    self.simpleExpr(node, addToIR)
                else:
                    [statements.append(stmt) for stmt in self.simpleExpr(node, addToIR)]

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
                    self.whileloop(node)
                else:
                    statements.append(self.whileloop(node))

            elif (node.name == 'dowhile'):
                if addToIR:
                    self.dowhile(node)
                else:
                    statements.append(self.dowhile(node))

            elif (node.name == 'forLoop'):
                if addToIR:
                    self.forloop(node)
                else:
                    statements.append(self.forloop(node))
            elif (node.name == 'break'):
                self.breakStmt(node)

            elif (node.name == 'continue'):
                self.continueStmt(node)
            
            # elif (node.name == 'ifstmt'):
            #     self.ifstmt(node)
            # else:
            #     print("Node ", node.name, " can not be converted")

        if not addToIR:
            return statements

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
                        if addToIR:
                            self.IRS.append(ir)
                        else:
                            statements.append(ir)
                    else:
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
                    print(ir)

                else:
                    operand2 = self.dequeue()
                    operand1 = self.dequeue()
                    operator = node.name
                    tempVar = 't_' + str(self.temporaryVarible)
                    ir = [tempVar, '=', operand1, operator, operand2]
                    print(ir)

                if addToIR:
                    self.IRS.append(ir)
                else:
                    statements.append(ir)
                self.enqueue(tempVar)
                self.temporaryVarible += 1
            elif(node.name == '-' and len(node.children) == 1):
                # Handle negative number
                operand1 = self.dequeue()
                operator = node.name
                self.enqueue(operator+operand1)
        self.dequeue()
        if addToIR:
            return tempVar
        else:
            return statements

    # Translate variable declaration without assignment into IR
    # Not necessary for the final IR
    # parameters: nodes, AST subtree with relevant parsed data
    def varDecl(self, nodes, addToIR=True):
        for node in nodes:
            if(node.name != None):
                if addToIR:
                    self.IRS.append(node.name)
                else:
                    return node.name

    # Translate goto statement into IR.
    # parameters: nodes, AST subtree with relevant parsed data
    def gotoStmt(self, nodes, addToIR=True):
        for node in nodes.children:
            if addToIR:
                self.IRS.append(['goto', node.name])
            else:
                return ['goto', node.name]

    # Create a label for goto statements, conditionals, or loops
    # parameters: nodes, AST subtree with relevant parsed data
    # parameters: type, determines whether or not to return the label
    # to the caller
    # If: type is loop label or condition label, return the label to caller
    # instead of appending to IR
    # Else if: label name already exists, creates the label with available name
    # (e.g 'goto even:', 'label even:')
    def createLabel(self, nodes, type, addToIR=True):
        if (type != None):
            loopL = 'L' + str(self.label) + ':'
            self.label += 1
            return loopL
        else:
            for node in nodes.children:
                if addToIR:
                    self.IRS.append([node.name, ':'])
                else:
                    return [node.name, ':']

    # Translate return statement into IR
    # parameters: nodes, AST subtree with relevant parsed data
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
    
    # Translates increment and decrement statements into IR
    def increment(self, nodes, name, addToIR=True):
        operator = name[0]
        for node in nodes.children:
            if addToIR:
                self.IRS.append([node.name, '=', node.name, operator, '1'])
            else:
                return [node.name, '=', node.name, operator, '1']

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

    def makeList(self, i):
        return [i]

    def merge(self, p1, p2):
        return sorted(p1 + p2)

    def backpatch(self, exprs, p, i):
        for k in p:
            exprs[k] = exprs[k].replace('_', i)

        return exprs

    # NOT SUPPORTED: negation of logical operators
    def condParse(self, cond, block):
        # Clear the queue
        self.queue = []
        stmts = {}
        negate = {
            '==':'!=',
            '!=':'==',
            '<':'>=',
            '>':'<=',
            '<=':'>',
            '>=':'<',
        }
        negAddrs = []
        
        if cond:
            for node in reversed(self.getSubtree(cond)):
                # print(node.name)
                # print(self.queue)

                if node.name == 'M':
                    # Node is conditional marker
                    continue
                elif node.name not in alc:
                    # Node is a variable
                    if (node.parent.name in logical):
                        # Node is an expression where var == 1 is true
                        expr = '{} == 1'.format(node.name)
                        stmts[self.instr] = 'if {} goto _'.format(expr)
                        self.enqueue([self.instr, expr, self.makeList(self.instr), self.makeList(self.instr + 1)])
                        stmts[self.instr + 1] = 'goto _'
                        self.instr += 2
                    else:
                        # Node is a variable in an arithmetic or comparison expression
                        self.enqueue((self.instr, node.name, [], []))
                elif node.name in arithmetic + comparison:
                    # Node is a non-logical operator
                    # E -> id1 relop id2
                    # 1. E.truelist = makelist(self.instr)
                    # 2. self.instr += 1
                    # 3. E.falselist = makelist(self.instr)
                    # 4. self.instr += 1
                    # 5. print('if {} {} {} goto _'.format(oper1, node.name, oper2))
                    # 6. print('goto _')

                    if (node.name == '~'):
                        oper = self.dequeue()
                        expr = '{} {}'.format(node.name, oper[1])
                        stmts[self.instr] = 'if {} goto _'.format(expr)
                        self.enqueue([self.instr, expr, self.makeList(self.instr), self.makeList(self.instr + 1)])
                        stmts[self.instr + 1] = 'goto _'
                        self.instr += 2
                    else:
                        oper2 = self.dequeue()
                        oper1 = self.dequeue()
                        expr = '{} {} {}'.format(oper1[1], node.name, oper2[1])
                        stmts[self.instr] = 'if {} goto _'.format(expr)
                        self.enqueue([self.instr, expr, self.makeList(self.instr), self.makeList(self.instr + 1)])
                        stmts[self.instr + 1] = 'goto _'
                        self.instr += 2
                else:
                    # Node is a logical operator
                    if (node.name == '!'):
                        # E -> NOT E1

                        # Don't want to dequeue; want to modify the enqueued entry
                        oper = self.queue[0]

                        if (isinstance(oper[1], list) is True):
                            # Operand is the result of a logical operation
                            addrs = oper[1]
                            for a in addrs:
                                # Append addr of expr that needs to be negated
                                if (a not in negAddrs):
                                    negAddrs.append(a)
                        else:
                            # Operand is an expression
                            expr = oper[1]
                            addr = oper[0]
                            for n in negate:
                                # Negate expression
                                if (n in stmts[addr]):
                                    expr = stmts[addr].replace(n, negate[n])
                                    stmts[addr] = expr
                                    break
                    elif(node.name == '&&'):
                        # E -> E1 && E2

                        e1 = self.dequeue()
                        e1addr, e1Truelist, e1Falselist = e1[0], e1[2], e1[3]
                        e2 = self.dequeue()
                        e2addr, e2Truelist, e2Falselist = e2[0], e2[2], e2[3]
                        eTruelist, eFalselist = [], []

                        # 1. backpatch(E1.truelist, e2.addr)
                        stmts = self.backpatch(stmts, e1Truelist, str(e2addr))
                        # 2. E.truelist = E2.truelist
                        eTruelist = e2Truelist
                        # 3. E.falselist = merge(E1.falselist, E2.falselist)
                        eFalselist = self.merge(e1Falselist, e2Falselist)

                        self.enqueue([self.instr, [e1addr, e2addr], eTruelist, eFalselist])
                    else:
                        # E -> E1 || E2

                        e1 = self.dequeue()
                        e1addr, e1Truelist, e1Falselist = e1[0], e1[2], e1[3]
                        e2 = self.dequeue()
                        e2addr, e2Truelist, e2Falselist = e2[0], e2[2], e2[3]
                        eTruelist, eFalselist = [], []

                        # 1. backpatch(E1.falselist, e2.addr)
                        stmts = self.backpatch(stmts, e1Falselist, str(e2addr))
                        # 2. E.truelist = merge(E1.truelist, E2.truelist)
                        eTruelist = self.merge(e1Truelist, e2Truelist)
                        # 3. E.falselist = E2.falselist
                        eFalselist = e2Falselist
                        
                        self.enqueue([self.instr, [e1addr, e2addr], eTruelist, eFalselist])
        # Negate expressions
        # print(negAddrs)
        for a in negAddrs:
            for n in negate:
                if (n in stmts[a]):
                    stmts[a] = stmts[a].replace(n, negate[n])
                    break

        return stmts

    # TODO: Add toggling for adding to IR after implementing adding to IR
    def condStmt(self, nodes, addToIR=True):
        output = []
        ifLabels = []
        firstFlag = True
        endIfLabel = self.instr
        self.instr += 1

        for i, stmt in enumerate(nodes):
            # Loop through if/else statements
            if (stmt.name == 'if' or stmt.name == 'else-if'):
                # Handle ifs and else ifs
                cond = stmt.children[0]
                block = self.statement(stmt.children[1], False)
                blockLabel = self.instr
                self.instr += 1

                stmts = self.condParse(cond, block)
                for k, v in stmts.items():
                    if (v == "goto _"):
                        # False jumps
                        if (i == len(nodes) - 1):
                            # Last condition; should jump to end of conditionals
                            v = v.replace('_', str(endIfLabel))
                        elif (i == len(nodes) - 2 and stmt.name == 'else-if'):
                            # Else if right before else; should jump to else block
                            v = v.replace('_', str(self.instr))
                        else:
                            # Any other case; should jump to next label
                            v = v.replace('_', str(self.instr + 1))
                    else:
                        # True jumps; should jump to block of conditional
                        v = v.replace('_', str(blockLabel))
                    if not firstFlag:
                        # Don't print the label for the very first if
                        output.append(["<{}>:".format(k)])
                    output.append([v])
                    firstFlag = False
                
                # Append label and escape goto to block
                block.insert(0, ["<{}>:".format(blockLabel)])
                block.append(['goto {}'.format(endIfLabel)])
                [output.append(s) for s in block]
            else:
                # Handle else
                blockLabel = self.instr
                block = self.statement(stmt.children[0], False)
                
                stmts = self.condParse(None, block)
                for k, v in stmts.items():
                    # if (v == "goto _"):
                    #     v = v.replace('_', str(blockLabel))
                    output.append(["<{}>:".format(k)])
                    output.append([v])
                
                block.insert(0, ["<{}>:".format(blockLabel)])
                block.append(['goto {}'.format(endIfLabel)])
                [output.append(s) for s in block]
        [self.IRS.append(s) for s in output]
        self.IRS.append(["<{}>:".format(endIfLabel)])
        # print(ifLabels)

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

    def getIR(self):
        str1 = " "
        indentFlag = 0
        for l in self.IRS:
            str2 = ''
            for elem in l:
                str2 += elem 
            
            if (''.join(str2) == '{'):
                indentFlag = 1
                str1 += str2 + '\n'
                continue
            elif (''.join(str2) == '}'):
                indentFlag = 0
                str1 += str2 + '\n'
                continue
            elif (indentFlag):
                str1 += '\t' + str2 + '\n'
            else:
                str1 += str2 + '\n'
        return str1

    # Read the IR from fileString into the IR structure
    def readIR(self, fileString):
        fileString = [x.strip() for x in fileString]  
        fileString = [x.replace('\t', ' ') for x in fileString]  
        for line in fileString:
            list = line.split()
            self.IRS.append(list)
