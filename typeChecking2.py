# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_parser import st
import re
import sys
class TypeChecking:
        def __init__(self, ast):
                self.treeString = ast.replace('"', '')

                self.tree = TreeNode.read(StringIO(self.treeString))
                self.numbersFloat = re.compile('\d+\.{1}\d+')
                self.numbersInt = re.compile('\d+')
                self.scope = 0
                # self.scope = 0
        def run(self):
                for node in self.tree.children:
                        if (node.name == '='):
                                # global variable
                                # print('global variable')
                                self.variablesTC(node.children)
                                # print(node.children)
                                continue
                        elif ( 'func-' in node.name):
                                self.scope += 1
                                print('func encountered')
                                continue
                        

        def variablesTC(self, nodes):
                supposedType = st.lookupTC(nodes[0].name, 0)
                self.checkType(nodes[1], supposedType)

        def checkType(self, expr, supposedType):
                if (supposedType == 'int'):
                        print('type of  ' + str(expr) +  '  supposed to be int')
                        expr = self.checkInt(expr)
                elif (supposedType == 'float'):
                        expr = self.checkFloat(expr)
                else:
                        pass
        def checkInt(self, expr):
                for node in expr.preorder():
                        if ('+-/*%'.find(node.name) != -1):
                                print(node.name)
                                print('what?')
                                continue
                        elif (self.numbersInt.match(node.name)):
                                print('expected int, matched int  ' + node.name)
                                continue
                        elif (self.numbersFloat.match(node.name)):
                                print('number is float. expected Int')
                                number = int(node.name)
                                node.name = str(number)
                        else:
                                type = st.lookupTC(node.name, self.scope)
                                if (type == 'Unknown'):
                                        print('unknown token found: ' + node.name)
                                elif (type == 'int'):
                                        print(' in else; in elif int')
                                        continue
                                else : 
                                        print('type conversion required')
                                        sys.exit(1)
                        return expr
        def checkFloat(self, expr):

                for node in expr.preorder():
                        if ('+-/*%'.find(node.name) != -1):
                                continue
                        elif (self.numbersInt.match(node.name)):
                                print('number is int. expected float')
                                number= int(node.name)
                                node.name = str(number) + '.' + '00'
                                continue
                        elif (self.numbersFloat.match(node.name)):
                                print('number is float. expected float ' + node.name)
                                continue
                        else:
                                type = st.lookupTC(node.name, self.scope)
                                if (type == 'Unknown'):
                                        print('unknown token found: ' + node.name)
                                elif (type == 'float'):
                                        continue
                                else : 
                                        print('type conversion required')
                                        sys.exit(1)
                        return expr
        



                                