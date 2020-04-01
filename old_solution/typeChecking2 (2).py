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
        with open('ast.txt', mode='w', encoding='utf-8') as f:
            self.tree.write(f, format='newick')

        with open('ast.txt', mode='r', encoding='utf-8') as f:
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
            elif (self.compOps.match(elem.name)):
                continue
            else:
                print('id encountered')
                continue
        return node

    def returnTC(self, nodes):
        supposedType = st.lookupTC(self.funcName, 0)
        # print(self.funcName)
        # print(supposedType)
        return self.checkType(nodes, supposedType)

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
        elif(supposedType == 'unsigned int'):
            return self.checkUInt(expr)
        else:
            print("Unknown type:   " + supposedType + '  ' + str(expr))
            # sys.exit(1)

    def checkInt(self, expr):
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
                else:

                    print('type conversion required for ' + str(node.name))
                    sys.exit(1)
        if (flag):
            expr = nodeList
        else:
            expr = nodeList[0]
        return expr

    def checkFloat(self, expr):
        flag = False
        if (isinstance(expr, list)):
            nodeList = expr
            flag = True
        else:
            nodeList = []
            nodeList.append(expr)
        for elem in expr:
            for node in elem.preorder():
                if ('+-/*%'.find(node.name) != -1):
                    continue
                elif (self.numbersFloat.match(node.name)):
                    print('number is float. expected float ' + node.name)
                    continue
                elif (self.numbersInt.match(node.name)):
                    print('number is int. expected float')
                    number = float(int(node.name))
                    node.name = str(number)
                    continue

                else:
                    Nodetype = st.lookupTC(node.name, self.scope)
                    if (Nodetype == 'Unknown'):
                        print('unknown token found: ' + node.name)
                    elif (Nodetype == 'float'):
                        continue
                    else:
                        print('type conversion required for ' + str(node.name))
                        sys.exit(1)
        if (flag):
            expr = nodeList
        else:
            expr = nodeList[0]
        return expr
    def checkUInt(self, expr):
        flag = False

        if (isinstance(expr, list)):
            nodeList = expr
            flag = True
        else:
            nodeList = []
            nodeList.append(expr)
        for elem in expr:
            for node in elem.preorder():
                if ('+-/*%'.find(node.name) != -1):
                    continue
                elif (self.numbersInt.match(node.name)):
                    print('number is unsigned int. expected unsigned int ' + node.name)
                    continue
                elif (self.numbersFloat.match(node.name)):
                    print('number is float. expected int')
                    number = float(int(node.name))
                    node.name = str(number)
                    continue

                else:
                    Nodetype = st.lookupTC(node.name, self.scope)
                    if (Nodetype == 'Unknown'):
                        print('unknown token found: ' + node.name)
                    elif (Nodetype == 'unsigned int'):
                        continue
                    else:
                        print('type conversion required for ' + str(node.name))
                        sys.exit(1)
        if (flag):
            expr = nodeList
        else:
            expr = nodeList[0]
        return expr

    def checkLong(self, expr):
        flag = False

        if (isinstance(expr, list)):
            nodeList = expr
            flag = True
        else:
            nodeList = []
            nodeList.append(expr)
        for elem in expr:
            for node in elem.preorder():
                if ('+-/*%'.find(node.name) != -1):
                    continue
                elif (self.numbersFloat.match(node.name)):
                    print('number is float. expected float ' + node.name)
                    continue
                elif (self.numbersInt.match(node.name)):
                    print('number is int. expected float')
                    number = float(int(node.name))
                    node.name = str(number)
                    continue

                else:
                    Nodetype = st.lookupTC(node.name, self.scope)
                    if (Nodetype == 'Unknown'):
                        print('unknown token found: ' + node.name)
                    elif (Nodetype == 'float'):
                        continue
                    else:
                        print('type conversion required for ' + str(node.name))
                        sys.exit(1)
        if (flag):
            expr = nodeList
        else:
            expr = nodeList[0]
        return expr
    def checkLongLong(self, expr):
        flag = False

        if (isinstance(expr, list)):
            nodeList = expr
            flag = True
        else:
            nodeList = []
            nodeList.append(expr)
        for elem in expr:
            for node in elem.preorder():
                if ('+-/*%'.find(node.name) != -1):
                    continue
                elif (self.numbersFloat.match(node.name)):
                    print('number is float. expected float ' + node.name)
                    continue
                elif (self.numbersInt.match(node.name)):
                    print('number is int. expected float')
                    number = float(int(node.name))
                    node.name = str(number)
                    continue

                else:
                    Nodetype = st.lookupTC(node.name, self.scope)
                    if (Nodetype == 'Unknown'):
                        print('unknown token found: ' + node.name)
                    elif (Nodetype == 'float'):
                        continue
                    else:
                        print('type conversion required for ' + str(node.name))
                        sys.exit(1)
        if (flag):
            expr = nodeList
        else:
            expr = nodeList[0]
        return expr
        
    def checkDouble(self, expr):
        flag = False

        if (isinstance(expr, list)):
            nodeList = expr
            flag = True
        else:
            nodeList = []
            nodeList.append(expr)
        for elem in expr:
            for node in elem.preorder():
                if ('+-/*%'.find(node.name) != -1):
                    continue
                elif (self.numbersFloat.match(node.name)):
                    print('number is float. expected float ' + node.name)
                    continue
                elif (self.numbersInt.match(node.name)):
                    print('number is int. expected float')
                    number = float(int(node.name))
                    node.name = str(number)
                    continue

                else:
                    Nodetype = st.lookupTC(node.name, self.scope)
                    if (Nodetype == 'Unknown'):
                        print('unknown token found: ' + node.name)
                    elif (Nodetype == 'float'):
                        continue
                    else:
                        print('type conversion required for ' + str(node.name))
                        sys.exit(1)
        if (flag):
            expr = nodeList
        else:
            expr = nodeList[0]
        return expr