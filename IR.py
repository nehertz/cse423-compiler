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
                # for node in self.tree.traverse():
                for node in self.tree.children:
                        
                        # handle function name node 
                        if ('func-' in str(node.name)):
                                self.funcNode(node, node.name)
                        # handle global varible node
                        elif (node.name == 'varDecl'):
                                self.varDecl(node)
        

        def funcNode(self, nodes, funcName):
                # funcName = ''
                funcName = funcName.replace('func-', '')
                for node in nodes.traverse():
                        
                        if (node.name == 'args'):
                                print("here")
                                self.args(node, funcName)

                        if (node.name == 'stmt'):
                                print("here1")
                                self.statement(node)
                        
        
        def args(self, node, funcName):
                argsCount = 0
                ir = []
                ir.append(funcName)
                for nodes in self.getSubtree(node):
                        if (nodes.name != 'args'):
                                self.enqueue(nodes.name)
                                argsCount += 1
                ir.append('(')
                while argsCount > 0:
                        ir.append(str(self.dequeue()))
                        if argsCount != 1:
                                ir.append(',')
                        argsCount -= 1
                ir.append(')')
                self.IRS.append(ir)
                # print(argsCount)                


        def statement(self, node):
                for nodes in node.traverse():
                        # in statement block, handle var decl with assignment
                        # note: only handles:
                        # int a = expr or a = expr, since the root used to 
                        # distinguish the node is assignment operator  
                        if (nodes.name in assignment):
                                self.assign(nodes)

                        # handle the var-decl without assignment case
                        # TODO: need to consider more cases. Only handles the simple one for now. 
                        elif (nodes.name == 'varDecl'):
                                pass
                                # self.varDecl(nodes)

        def assign(self, node):
                subtree = self.getSubtree(node)
                for nodes in reversed(subtree):
                        if( nodes.name not in operators.keys()):
                                self.enqueue(nodes.name)

                        elif(nodes.name not in assignment and nodes.name in operators.keys()):
                                operand2 = self.dequeue()
                                operand1 = self.dequeue()
                                operator = nodes.name
                                tempVar = 't_' + str(self.temporaryVarible)
                                ir = [tempVar, '=', operand1, operator, operand2]
                                self.IRS.append(ir)
                                self.enqueue(tempVar)
                                self.temporaryVarible += 1
                        elif(nodes.name in assignment):
                                if(nodes.name == '='):
                                        operand1 = self.dequeue()
                                        operand2 = self.dequeue()
                                        ir = [operand2, '=', operand1]
                                        self.IRS.append(ir)
                                else:
                                        # e,g : if we have +=, operator1 is '+', operator2 is '='
                                        operator1 = nodes.name[0]
                                        operator2 = nodes.name[1]
                                        operand1 = self.dequeue()
                                        operand2 = self.dequeue()
                                        # print("operand1 ", operand1)
                                        # print("operand2 ", operand2)
                                        ir = [operand2, '=', operand2, operator1, operand1] 
                                        self.IRS.append(ir)

        def varDecl(self, nodes):
                for node in nodes:
                        self.IRS.append([node.name])


        def getSubtree(self, node):
                subtree = []
                for nodes in node.levelorder():
                        subtree.append(nodes)
                return subtree
                
        def enqueue(self, item):
                self.queue.append(item)
        
        def dequeue(self):
                return self.queue.pop(0)
                
        def printIR(self):
                str1 = " " 
                for list in self.IRS:
                        print(str1.join(list))
                        