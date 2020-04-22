"""
Checks types of every expression. 
Approach used: Reads the AST, then 2 types are handled:
- Variable assignment/declaration: When variable is declared with an assignment,
    the variables type is compared with the rvalue. The type of expression is evaluated by
    traversing the subtree and checking every ID/NUMCONST's type using either Symbol Table (for identifiers)
    and regex (for NUMCONST)
    - same applies to variable assignment. lvalue type is obtained using the symbol table and variable scope is 
        calculated based on the number of functions encountered. i.e. if there are 2 functions defined before main, 
        then the variable declared in main will have a scope of 3. The symbol table has a special function for TypeChecking, 
        where this scoping mechanism is implemented identically.
- Function TypeChecking: Function type checking is implemented for return statement. If the expression for return statement 
    matches the Function return type, then the function is OK, otherwise type-conversion of the expression is required. 
-Type Conversion: We have only implemented type conversion for Numconst from int to float and vice versa. This change will also
  be reflected in the AST and that's why the run() method returns the AST in newick form.
"""

# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_parser import st
import re
import sys
import bitstring
from typeConversion import TypeConversion

class TypeChecking:
    st = st
    def __init__(self, ast):
        self.treeString = ast.replace('"', '')
        self.tree = TreeNode.read(StringIO(self.treeString))
        self.numbersFloat = re.compile(r'\d+\.{1}\d+')
        self.numbersInt = re.compile(r'^[-]{0,1}\d+')
        self.arithOps = re.compile(r'[\/\+\-\*\%]')
        self.logicalExpr = re.compile(r'(\|\|)|(&&)|(\!)')
        self.bitOps = re.compile(r"(<<)|(>>)|(&)|(\|)|(\^)|(~)")
        self.compOps = re.compile(r'(==)|(\!=)|(>=)|(<=)')
        self.typeConversion = TypeConversion()
        # global scope = 0
        # scope is incremented as the functions are encountered.
        self.scope = 0
        # Function name is stored
        self.funcName = ''

    def run(self):
        '''
        returns the modified AST which reflects the type-conversion
        NOTE: ast.txt file is created and will have the newick form written in it. 
        Currently skbio.tree doesn't have any other methods with which we can store 
        the newick string to a variable. 
        Quite inefficient, but works! 
        '''
        for node in self.tree.children:
            if (node.name == '='):
                # Variable assignment / Declaration w assignment is handled 
                # variable could either be local or global 
                # Both have the same implementation
                node.children = self.variablesTC(node.children)
                continue
            elif ('func-' in node.name):
                # Scope is incremented
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
        '''
        Checks for the scope of function
        '''
        for node in nodes:
            if ('stmt' in node.name):
                node.children = self.checkStatement(node.children)
                continue
        return nodes

    def checkStatement(self, nodes):
        '''
        Handles the statements for now. 
        TODO: switch statements
        '''
        for node in nodes:
            if ('=' == node.name):
                node.children = self.variablesTC(node.children)
                # print(node.children)
                continue
            elif ('return' == node.name):
                node.children = self.returnTC(node.children)
                continue
            elif ('ifstmt' == node.name):
                node.children = self.checkConditionals(node.children)
                continue
            elif ('while' == node.name):
                print('while: ' + str(node.children[0]))
                node.children[0] = self.checkLogicalExpr(node.children[0])
                if (node.children[1] == 'stmt'):
                    child1 = node.children[1]
                    child1.children = self.checkStatement(child1.children)
            elif ('forLoop' == node.name):
                node = self.checkForLoop(node)
            elif ('++' == node.name or '--' == node.name):
                node.children[0] = self.checkType(node.children[0], 'int')
        return nodes

    def checkForLoop(self, node):
        '''
        checks init, conditional, increment and scope of the loop. 
        '''
        body = node.children[0]
        # init = node.children[1]
        increment = node.children[2]
        conditional = node.children[3]

        body.children = self.checkStatement(body.children)
        # id = init.children[0].children[0].children[0]
        increment.children = self.checkStatement(increment.children)
        conditional.children[0] = self.checkLogicalExpr(conditional.children[0])
        
        node.children[0] = body
        node.children[2] = increment
        node.children[3] = conditional
        return node


    def checkConditionals(self, nodes):
        '''
        For if statements or any loops, it checks for condition of the control statements
        '''
        for node in nodes:
            if (node.name == 'if' or node.name == 'elseif'):
                node.children[0] = self.checkLogicalExpr(node.children[0])
                child1 = node.children[1]
                if ('stmt' == child1.name):
                    child1.children = self.checkStatement(child1.children)
            elif (node.name == 'else'):
                child1 = node.children[0]
                if ('stmt' == child1.name):
                    child1.children[0] = self.checkStatement(child1.children[0])
            else:
                continue
        return nodes

    def checkLogicalExpr(self, node):
        '''
        Checks logical expression types. Not really needed, but there to support for later updates
        '''
        # print('in checkLogicalExpr:   ' + str(node))
        for elem in node.traverse():
            if (self.logicalExpr.match(elem.name)):
                continue
            elif (self.compOps.match(elem.name)):
                continue
            else:
                # print('id encountered')
                continue
        return node

    def returnTC(self, nodes):
        '''
        Checks for return type of function by using SymbolTable's lookupTC() method.
        It sends 0 as the scope because 0 is defined as default global scope which is 
        where the functions are declared/defined.
        After obtaining type, it sends the rvalue to checkType()
        '''
        supposedType = st.lookupTC(self.funcName, 0)
        nodes[0] = self.checkType(nodes[0], supposedType)
        return nodes

    def variablesTC(self, nodes):
        '''
        Checks for the lvalue variable's type from SymbolTable. The scope here is 
        incremented as the functions are encountered in self.run()
        Sends the variable to checkType()
        '''
        supposedType = st.lookupTC(nodes[0].name, self.scope)        
        # print('node.name = ' + nodes[0].name + '  type: ' + supposedType)
        nodes[1] = self.checkType(nodes[1], supposedType)
        # print(nodes[1])
        return nodes


    def checkType(self, expr, supposedType):
        '''
        Traverses till the leaves nodes and checks each node's type and compare it with the l-value's type.
        If not the same conversion happens 
        '''
        flag = False 
        if (isinstance(expr, list)):
            nodeList = expr 
            flag = True 
        else:
            nodeList = []
            nodeList.append(expr)
        for node in expr.preorder():
            if ('+-/*%'.find(node.name) != -1):
                continue 
            elif (self.logicalExpr.match(node.name) != None):
                continue 
            elif (self.compOps.match(node.name) != None):
                continue 
            elif(self.bitOps.match(node.name) != None):
                continue
            elif(self.numbersFloat.match(node.name) != None):
                if (supposedType == 'float' or supposedType == 'double'):
                    continue 
                else:
                    # print("number is float expected " + supposedType)
                    node.name = self.convertType(node.name, 'float', supposedType)
                    continue 
            elif(self.numbersInt.match(node.name) != None):
                node.name = self.convertType(node.name, 'int', supposedType)
            else:
                if ('func-' in node.name):
                    # print(node.children)
                    # self.funcCall(node)
                    funcName = node.name.replace('func-', '')
                    # self.funcCall(node,funcName, st.get_fds(funcName))
                    self.funcCall(funcName, node, st.get_fds(funcName))
                    typeFunction = st.lookupTC(funcName, 0)
                    # if (typeFunction != supposedType):
                    node.name = self.convertTypeID(node.name, typeFunction, supposedType)
                    break
                typeNode = st.lookupTC(node.name, self.scope)
                # print('node.name = ' + node.name)
                if (typeNode == 'Unknown'):
                    print('unknown token found : ' + node.name)
                    # sys.exit(1)
                else:
                    node.name = self.convertTypeID(node.name, typeNode, supposedType)
        if (flag):
            return nodeList 
        else:
            return nodeList[0]
        
    def funcCall(self, funcName, node, fds):
        '''
        implementation if RHS is a function call
        To check: Number of parameters 
        Types of parameters
        return value of the function
        '''
        args_count = fds.get_argc()
        expected_args = fds.get_vars_type()
        args = node.children[0].children
        if (len(args) == args_count):
            for item1, item2 in zip(args, expected_args):
                item1 = self.checkType(item1, item2)
        else:
            print('error: Not enough arguments for function call ' + funcName)
            sys.exit(1) 
        
    def convertType(self, expr, fromType, toType):
        '''
        converts type from fromType to toType using typeconversion class. 
        '''
        if (fromType == toType):
            return expr
        fromType = self.stringFormat(fromType)
        toType = self.stringFormat(toType)
        funcString = 'convert' + fromType + '2' + toType
        # https://stackoverflow.com/questions/4246000/how-to-call-python-functions-dynamically
        # the function name is generated dynamically and are being called dynamically with expr as 
        # a parameter
        # i.e. expr = self.typeConversion.funcString(expr)
        expr = getattr(self.typeConversion, funcString)(expr)
        return expr
        
    def convertTypeID(self, expr, fromType, toType):
        '''
        converts type from fromType to toType
        Just performs type-casting
        '''
        
        if (fromType == toType):
            return expr 
        expr = '(' + toType + ') ' + expr
        return expr
    
    def stringFormat(self, typeString):
        '''
        makes the string into an appropriate form
        '''
        
        typeString = typeString.replace('unsigned ', 'U')
        typeString = typeString.replace('int', 'Int')
        typeString = typeString.replace('signed', '')
        typeString = typeString.replace('double', 'Double')
        typeString = typeString.replace('float', 'Float')
        typeString = typeString.replace('long', 'Long')
        typeString = typeString.replace('Long Long', 'LongLong')
        typeString = typeString.replace('char', 'Char') 
        typeString = typeString.replace('short', 'Short')
        return typeString


        
