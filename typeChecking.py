# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
import re
# from ply_parser import st

class typeChecking:
        def __init__(self):
                self.flag = True
        def checkTypes(self, treeString, st):
                tree = TreeNode.read(StringIO(treeString))
                count = 0
                assignOps = re.compile("(=)|(\+=)|(-=)|(\*=)|(/=)|(%=)|(<<=)|(>>=)|(&=)|(\^=)|(\|=)")
                operations = re.compile("(\|\|)|(&&)|(<<)|(>>)|(&)|(\|)|(\^)|(\/)|(\+)|(\-)|(\*)|(\%)|(==)|(!=)|(>=)|(<=)")
                for node in tree.preorder():
                        if (assignOps.match(node.name)):
                                continue
                        else: 
                                count +=1
                                if (count == 1):
                                        type1 = st.lookup(node.name)
                                elif(count >= 2):
                                        # if ('+-*/%&|^'.find(node.name) != -1):
                                        if (operations.match(node.name)):
                                                continue
                                        else:
                                                if (self.getTypeSimilarity(type1, node.name, st)):
                                                        # print("good")
                                                        continue
                                                else:
                                                        # print ("not good")
                                                        print("types not matched. Type conversion required which is not supproted")
                                                        continue

        
        def getTypeSimilarity(self, type1, token, st):
                number = re.compile('\d+.{0,1}\d*')
                if (number.match(token)):
                        print("it's a number  " + token)
                        return False 
                else:
                        type2 = st.lookup(token)
                        if (type1 == type2):
                                print('types matched   ' + token)
                                return True 
                        else: 
                                print('types not matched   ' + token)
                                return False
