from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_scanner import assignment
from ply_scanner import operators


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
                for node in nodes.traverse():
                        if (node.name == 'args'):
                                self.args(node, funcName)
                        if (node.name == 'stmt'):
                                self.statement(node)
                self.IRS.append(['}'])
                        
        
        def args(self, nodes, funcName):
                argsCount = 0
                ir = []
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
                        # in statement block, handle var decl with assignment
                        # note: only handles:
                        # int a = expr or a = expr, since the root used to 
                        # distinguish the node is assignment operator  
                        if (node.name in assignment):
                                self.assign(node)

                        # handle the var-decl without assignment case
                        # TODO: need to consider more cases. Only handles the simple one for now. 
                        elif (node.name == 'varDecl'):
                                self.varDecl(node)
                        elif (node.name == 'return'):
                                self.returnStmt(node)

        def assign(self, nodes):
                subtree = self.getSubtree(nodes)
                operand2 = ''
                for node in reversed(subtree):
                        if( node.name not in operators.keys()):
                                self.enqueue(node.name)
                        elif(node.name not in assignment and node.name in operators.keys()):
                                operand2 = self.dequeue()
                                operand1 = self.dequeue()
                                operator = node.name
                                tempVar = 't_' + str(self.temporaryVarible)
                                ir = [tempVar, '=', operand1, operator, operand2]
                                self.IRS.append(ir)
                                self.enqueue(tempVar)
                                self.temporaryVarible += 1
                        elif(node.name in assignment):
                                if(node.name == '='):
                                        operand1 = self.dequeue()
                                        operand2 = self.dequeue()
                                        ir = [operand2, '=', operand1]
                                        self.IRS.append(ir)
                                else:
                                        # e,g : if we have +=, operator1 is '+', operator2 is '='
                                        operator1 = node.name[0]
                                        operator2 = node.name[1]
                                        operand1 = self.dequeue()
                                        operand2 = self.dequeue()
                                        ir = [operand2, '=', operand2, operator1, operand1] 
                                        self.IRS.append(ir)
                return operand2

        def varDecl(self, nodes):
                for node in nodes:
                        if(node.name != None):
                                self.IRS.append([node.name])

        # TODO: return statement needs to support var assign and func calls 
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
                                self.funcCall(node)
                               
                        else:
                                self.IRS.append(['ret', node.name])
                

        def funcCall(self, nodes):
                pass

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