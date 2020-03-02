# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
# from ply_parser import st

class typeChecking:
        def __init__(self):
                self.flag = True
        def checkTypes(self, treeString, st):
                tree = TreeNode.read(StringIO(treeString))
                count = 0
                for node in tree.preorder():
                        if (node.name == '='):
                                continue
                        else: 
                                count +=1
                                if (count == 1):
                                        type1 = st.lookup(node.name)
                                elif(count >= 2):
                                        if ('+-*/'.find(node.name) != -1):
                                                
                                        