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
                for node in self.tree.traverse():
                        if (node.name == 'stmt'):
                                self.statementNode(node)
        
        def statementNode(self, node):
                for nodes in node.traverse():
                        if (nodes.name in assignment):
                                self.assign(nodes)

        def assign(self, node):
                subtree = self.getSubtree(node)
                for nodes in reversed(subtree):
                        if( nodes.name not in operators.keys()):
                                self.enqueue(nodes.name)

                        elif(nodes.name not in assignment and nodes.name in operators.keys()):
                                operand1 = self.dequeue()
                                operand2 = self.dequeue()
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
                        