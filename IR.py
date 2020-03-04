
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode

class IR:
        def __init__(self, ast):
                self.IRStructure = []
                ast = ast.replace('\"', '')
                self.tree = TreeNode.read(StringIO(ast))
                self.variables = 1

        def run(self):
                for node in self.tree.traverse():
                        if (node.name == 'stmt'):
                                self.statementNode(node)
                

        def statementNode(self, node):
                # equalNode = node.neighbors()
                equalEncountered = False
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
                for node1 in exprNode.tips():
                        siblings = node1.siblings()
                        parent = node1.ancestors()[0]
                        s = '_' + str(self.variables)
                        self.variables += 1

                        if ('+-/*'.find(parent.name) != -1):
                                s = s + ' = ' + node1.name + ' ' + parent.name + ' ' + siblings[0].name
                        print(s)