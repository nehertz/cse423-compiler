'''
SymbolTable.py contains a list of the tuples. Each typle contain identifier name, type of the identifier, and 
scope of the identifier. 
Scope is defined as the following:
 -Default global Scope = 0
 -function scope is incremented as the function is encountered. i.e. If there are two functions defined before main,
    the scope of the variables defined in main() will be 3.
 - Nested Scope is defined by LSHIFTing the current scope to 1. i.e. if there's a variable defined in a while loop inside of main,
 assuming no other functions are defined before main, then the scope of the variables will start at 11. Nested scope always performs 
 LSHIFTING. 
    - Getting out of scope is defined as RSHIFT. nestedScope >>= 1 is done when RBRACE is encountered. If no corresponding LBRACE is found,
    then error occurs.
- EXTRA: loops, conditionals or any other type of scope can not be defined in global scope (weak implementation)
'''
import sys
from functionDS import functionDS
class SymbolTable:
    def __init__(self):
        '''
        Defined three scopes: global scope, currentScope, nested scope
        '''
        self.symbolTable = []
        self.functions= []
        self.currentScope = 0
        self.globalScope = 0
        self.nestedScope = 0b0
        self.args = []
        self.afterVarAssign = True
        self.ID = ''
        self.functionParam = False
        self.fds = None

    def insert(self, token, type, scope=-1):
        '''
        if scope = -1, then the declaration occurs inside of a scope i.e. function, loop, or conditionals.
        else the declaration occurs in a global scope.
        '''
        if (self.lookup(token) != None):
            print("error: token already declared")
            sys.exit(1)
        if (scope == -1):
            if (self.nestedScope == 0b0):
                self.symbolTable.append(
                    (token, type, str(self.currentScope), str(self.currentScope)))
            else:
                self.symbolTable.append((token, type, str(self.currentScope) + str(self.nestedScope), str(self.currentScope)))
        else:
            self.symbolTable.append((token, type, scope, str(0)))

    '''
    lookup function is called from ply_parser() and looks up the token from the table
    '''
    def lookup(self, token):
        acceptableScopes = []
        nested = self.nestedScope
        if (nested == 0):
            acceptableScopes.append(str(self.currentScope))
        else:
            acceptableScopes.append(str(self.currentScope))
            while (nested != 0):
                acceptableScopes.append(str(self.currentScope) + str(nested))
                nested >>= 1
        acceptableScopes.append(str(0))

        for elem in self.symbolTable:
            if ((elem[0] == token) and (elem[2] in acceptableScopes)):
                # print("found: {0} with type: {1} in scope {2}".format(elem[0], elem[1], elem[2]))
                return elem[1]
        print("{0} not found in the symbol table ".format(token))
        return None

    def print(self):
        print(self.symbolTable)
        for fds in self.functions:
            print('1 + ')
            fds.print()

    def symbolTableConstruct(self, p, type):
        ''' 
        SymbolTable is constructed with ply_parser.py 
        For function declaration, function is added to the table with 0 scope
        For variable declaration w definition, variable is added to the symbol table with scope details.
        '''
        if (type == 'varDecl'):
            # if (len(p) == 3):
            if (self.ID != '' and self.afterVarAssign):
                self.insert(self.ID, p[1])
                self.ID = ''
                self.afterVarAssign = False
                return
            # elif (self.functionParam):
            #     self.insert(str(p[2]), str(p[1]))
            #     self.fds.add_vars_type(str(p[1]))
            else:
                self.insert(str(p[2]), str(p[1]))

        if (type == 'funcDecl'):
            if (self.globalScope == 1):
                # self.fds = functionDS(str(p[2]))
                # self.functions.append(self.fds)   
                if (self.fds.get_name() == 'Unknown'):
                    self.fds.set_name(str(p[2]))
                    self.fds.set_returnType(str(p[1]))
                self.insert(str(p[2]), str(p[1]), self.globalScope - 1)
                self.fds = None
            else:
                print("error: function definition not in a global scope")
                sys.exit(1)

        if (type == 'typeSpecList'):
            if (len(p) == 5):
                self.args.append((p[4], p[3]))
            elif (len(p) == 3):
                self.args.append((p[2], p[1]))
            else:
                print("typespec list: unexpected")
                sys.exit(1)
                return

    def symbolTable_afterVarAssign(self):
        self.afterVarAssign = True

    def symbolTable_varAssign(self, ID):
        self.ID = str(ID)
        return

    def inScope(self):
        self.currentScope += 1
        self.globalScope = 0
        self.fds = functionDS('Unknown')
        self.functions.append(self.fds)
        if (len(self.args) != 0):
            for elem in self.args:
                self.fds.add_vars_type(elem[1])
                self.insert(elem[0], elem[1])
            self.args.clear()
        return

    def outScope(self):
        if (self.nestedScope != 0b0):
            print("error: missing rbrace")
            sys.exit(1)
        self.globalScope = 1
        return

    def loopInScope(self):
        if (self.currentScope == 0):
            # print("error: unexpected loop {0}.{1}".format(p.lineno, p.lexpos))
            print("error: unexpected loop ")
        else:
            self.nestedScope = (self.nestedScope << 1) | 0b1

        return

    def loopOutScope(self):
        if (self.nestedScope == 0b0):
            print("error: No matching left brace found")
        else:
            self.nestedScope >>= 1
        return

    def lookupTC(self, token, scope):
        '''
        This method is useful for type_checking in the later phase.
        Here the scope is incremented as one function is encountered and nestedscope serves
        no purpose. So the scope is compared with the parameter and then token is compared.
        '''
        token = token.replace(';', '')
        for elem in self.symbolTable:
            if ((elem[0] == token) and (elem[3] == str(scope))):
                return elem[1] 

        return 'Unknown'
    
    def startFunctionParam(self):
        # print('function parameters begin')
        self.functionParam = True

    def endFunctionParam(self):
        # print('function parameters end')
        self.functionParam = False

    def get_fds(self, name):
        # print(name) 
        for fds in self.functions:
            E_name = fds.get_name()
            # print(E_name)
            if (E_name == name):
                return fds 
        print('func name not found  ' + name)
        sys.exit(1)