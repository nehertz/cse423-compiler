
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode

class IR:
        def __init__(self, ast):
                self.IRStructure = []
                self.tree = TreeNode.read(StringIO(ast))


        def run(self):
                for node in self.tree.traverse():
                        if (node.name == 'stmt'):
                                self.statementNode(node)
                

        def statementNode(self, node):
                equalNode = node.neighbors()
                print(equalNode)
                # if ('=' in equalNode):
                #         for node1 in equalNode.tips():
                #                 print(node1.name)