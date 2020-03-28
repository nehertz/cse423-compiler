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
        self.logicalExpr = re.compile(r'(\|\|)|(&&)|(\!)')
        self.compOps = re.compile(r'(==)|(\!=)|(>=)|(<=)')
        self.scope = 0
        self.funcName = ''


    def run(self):
        for node in self.tree.children:
            if (node.name == '='):
                node.children = self.variablesTC(node.children)
                continue 
            elif ('func-' in node.name):
                self.funcName = node.name.replace('func-', '')
                self.scope += 1
                node.children = self.functionsTC(node.children)
                continue 
            else:
                continue

        with open('ast.txt', mode='w', encoding='utf-8') as f:
            self.tree.write(f, format='newick')

        with open('ast.txt', mode='r', encoding='utf-8') as f:
            ast = f.readlines()

        return ast[0]

    def functionsTC(self, nodes):
        for node in nodes:
            if ('stmt' in node.name):
                node.children = self.checkStatement(node.children)
                continue 
        return nodes 
    
    def checkStatement(self, nodes):
        for node in nodes:
            if ('=' == node.name):
                node.children = self.variablesTC(node.children)
                continue 
            elif ('return' == node.name):
                node.children = self.returnTC(node.children)
                continue
            elif('ifStmt' == node.name):
                node.children = self.checkConditionals(nodes)
                continue 
            elif ('++' == node.name or '--' == node.name):
                node.children = self.checkInt(node.children)
        return nodes 


    def checkConditionals(self, nodes):
        for node in nodes:

            if (node.name == 'if' or node.name == 'elseif' or node.name == 'else'):
                node.children[0] = self.checkLogicalExpr(node.children[0])
            else:
                continue 
            return nodes 

    def checkLogicalExpr(self, node):
        for elem in node.traverse():
            if (self.logicalExpr.match(elem.name)):
                continue 
            elif(self.compOps.match(elem.name)):
                continue 
            else:
                print('id encountered')
                continue
        return node 
    
    def returnTC(self, nodes):
        supposedType = st.lookupTC(self.funcName, 0)
        return self.checkType(nodes, supposedType)

    def variablesTC(self, nodes):
        supposedType = st.lookupTC(nodes[0].name, self.scope)
        nodes[1] = self.checkType(nodes[1], supposedType)
        return nodes 
    def checkTypes(self, expr, supposedType):
        if (supposedType == 'float'):
            return self.checkFloat(expr)
        elif(supposedType == 'int' or supposedType == 'signed int'):
            return self.checkInt(expr)
        elif(supposedType == 'unsigned int'):
            return self.checkUInt(expr)
        elif (supposedType == 'double'):
            return self.checkDouble(expr)
        else: 
            print("Unknown Type: " + supposedType + ' ' + str(expr))
            sys.exit(1)
    def checkInt(self, expr):
        flag = False 
        if (isinstance(expr, list)):
            nodeList = expr 
            flag = True 
        else:
            nodeList = []
            nodeList.append(expr)

        for node in nodeList:
            if ('+-/*%'.find(node.name) != -1):
                continue 
            elif (self.numbersFloat.match(node.name) != None):
                print('number is float. expected int')
                number = int(float(node.name))
                node.name = str(number)
                continue 
            elif (self.numbersInt.match(node.name) != None):
                continue 
            else:
                typeNode = st.lookupTC(node.name, self.scope)
                if (typeNode == 'Unknown'):
                    print('unknown token found: ' + node.name)
                    continue 
                elif (typeNode == 'int'):
                    continue 
                else:
                    print('type conversion required for ' + str(node.name))
                    sys.exit(1)

        if (flag):
            expr = nodeList 
        else:
            expr = nodeList[0]
        return expr 


        