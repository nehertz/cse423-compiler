# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_parser import st
import re
import sys
import bitstring
class TypeChecking:
        def __init__(self, ast):
                self.treeString = ast.replace('"', '')

                self.tree = TreeNode.read(StringIO(self.treeString))
                self.numbersFloat = re.compile(r'\d+\.{1}\d+')
                self.numbersInt = re.compile(r'\d+')
                self.scope = 0
                self.funcName = ''
                # self.scope = 0
        def run(self):
                for node in self.tree.children:
                        # print(node)
                        if (node.name == '='):
                                # global variable
                                # print('global variable')
                                node.children = self.variablesTC(node.children)
                                # print(node.children)
                                continue
                        elif ('func-' in node.name):
                                # print(node.children)
                                self.funcName = node.name.replace('func-', '')
                                self.scope += 1
                                node.children = self.functionsTC(node.children)
                                continue
                        else: 
                                continue
                with open('ast.txt',mode='w', encoding='utf-8') as f:
                        self.tree.write(f, format='newick')
                        
                with open('ast.txt',mode='r', encoding='utf-8') as f:
                        ast = f.readlines()

                return ast[0]
                        

        def functionsTC(self, nodes):
                for node in nodes:
                        # print(node.name)
                        if ('stmt' in node.name):
                                # print(node.name)
                                node.children = self.checkStatement(node.children)
                                continue
                return nodes
        def checkStatement(self, nodes):
                for node in nodes:
                        # print(node.name)
                        if ('=' == node.name):
                                # print(node.name)
                                node.children = self.variablesTC(node.children)
                                continue
                        elif ('return' == node.name):
                                node.children = self.returnTC(node.children)
                                continue
                        elif ('ifStmt' == node.name):
                                # node.children = self
                                continue
                return nodes

        def returnTC (self, nodes):
                supposedType = st.lookupTC(self.funcName, 0)
                # print(self.funcName)
                # print(supposedType)
                return self.checkType(nodes, supposedType)

    def checkStatement(self, nodes):
        for node in nodes:
            # print(node.name)
            if ('=' == node.name):
                # print(node.name)
                self.variablesTC(node.children)
                continue
            elif ('return' == node.name):
                self.returnTC(node.children)
                continue

        def variablesTC(self, nodes):
                supposedType = st.lookupTC(nodes[0].name, self.scope)
                # print(supposedType + '   token:   ' + nodes[0].name)
                # print(nodes[1])
                nodes[1] = self.checkType(nodes[1], supposedType)
                return nodes

        def checkType(self, expr, supposedType):
                if (supposedType == 'float'):
                        # print(expr)
                        return self.checkFloat(expr)
                elif (supposedType == 'int'):
                        # print('type of  ' + str(expr) +  '  supposed to be int')
                        return self.checkInt(expr)


                else:
                        print("Unknown type:   " + supposedType + '  ' + str(expr))
                        # sys.exit(1)
        def checkInt(self, expr):
                print('in checkInt')
                print(type(expr))
                flag = False
                if (isinstance(expr, list)):
                        nodeList = expr
                        flag = True
                else:
                        nodeList = []
                        nodeList.append(expr)
                # for elem in expr:
                for node in nodeList:
                        if ('+-/*%'.find(node.name) != -1):
                                # print(node.name)
                                # print('what?')
                                continue
                        elif (self.numbersFloat.match(node.name) != None):
                                print('number is float. expected Int')
                                number = int(float(node.name))
                                # print(number)
                                node.name = str(number)
                                print('in checkint   ' + node.name)
                                continue
                        elif (self.numbersInt.match(node.name) != None):
                                # print('expected int, matched int  ' + node.name)
                                continue

                        else:
                                typeNode = st.lookupTC(node.name, self.scope)
                                if (typeNode == 'Unknown'):
                                        print('unknown token found: ' + node.name)
                                        continue
                                elif (typeNode == 'int'):
                                        # print(' in else; in elif int')
                                        continue
                                else : 
                                        print('type conversion required')
                                        # sys.exit(1)
                if (flag):
                        expr = nodeList
                else:
                        expr = nodeList[0]
                return expr
        def checkFloat(self, expr):
                for elem in expr:
                        for node in elem.preorder():
                                if ('+-/*%'.find(node.name) != -1):
                                        continue
                                elif (self.numbersFloat.match(node.name)):
                                        print('number is float. expected float ' + node.name)
                                        continue
                                elif (self.numbersInt.match(node.name)):
                                        print('number is int. expected float')
                                        number= float(int(node.name))
                                        node.name = str(number)
                                        print(number)
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
        

    def checkFloat(self, expr):

        for node in expr.preorder():
            if ('+-/*%'.find(node.name) != -1):
                continue
            elif (self.numbersFloat.match(node.name)):
                print('number is float. expected float ' + node.name)
                continue
            elif (self.numbersInt.match(node.name)):
                print('number is int. expected float')
                number = float(int(node.name))
                node.name = str(number)
                print(number)
                continue

            else:
                type = st.lookupTC(node.name, self.scope)
                if (type == 'Unknown'):
                    print('unknown token found: ' + node.name)
                elif (type == 'float'):
                    continue
                else:
                    print('type conversion required')
                    sys.exit(1)
            return expr
