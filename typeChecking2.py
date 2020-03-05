# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode

class TypeChecking:
        def __init__(self, ast):
                self.treeString = ast.replace('"', '')
                self.tree = TreeNode.read(StringIO(self.treeString))
                
        def run(self):
                for node in self.tree.children:
                        print(node.name)