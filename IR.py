
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from skbio.tree import MissingNodeError
class IR:
        def __init__(self, ast):
                self.IRStructure = []
                ast = ast.replace('\"', '')
                self.tree = TreeNode.read(StringIO(ast))
                self.variables = 1

        def run(self):
                for node in self.tree.traverse():
                        if (node.name == 'stmt'):
                                for child in node.children:
                                        self.statementNode(child)
                                        
                                        # if (node.distance(self.tree.find(name)) <= 2):
                                                # print(name)
                

        def statementNode(self, node):
                # equalNode = node.neighbors()
                equalEncountered = False
                exprNode = TreeNode()
                expr = False
                for node1 in node.traverse():
                        if (node1.name == '='):
                                equalEncountered = True
                                continue 
                        if (equalEncountered):
                                equalEncountered = False 
                                expr = True
                                continue
                        if (expr):
                                exprNode = node1
                                print('in here')
                                break
                # copy_exprNode = exprNode.copy()
                # notFound = False
                seenNodes = []
                for node1 in exprNode.tips():
                        if (node1 in seenNodes):
                                continue
                        siblings = node1.siblings()
                        parent = node1.ancestors()[0]
                        # exprNode.remove(siblings[0])
                        seenNodes.append(siblings[0])
                        
                        s = '_' + str(self.variables)
                        self.variables += 1
                        if ('+-/*'.find(parent.name) != -1):
                                s = s + ' = ' + node1.name + ' ' + parent.name + ' ' + siblings[0].name
                        print(s)
