'''
SymbolTable.py contains a list of the tuples. 
Each typle contain identifier name, type of the identifier, and scope of the identifier. 
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
- Checks if the variable is in the scope or not
- Makes use of functionDS to store the number of parameters, types of each parameter and the return type of function.
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
        
        # for multivariable declaration with same type
        self.sameType = None
        self.sameIDs = []

    def insert(self, token, type, scope=-1):
        '''
        if scope = -1, then the declaration occurs inside of a scope i.e. function, loop, or conditionals.
        else the declaration occurs in a global scope.
        '''
        if (self.lookup(token) != None):
            print("error: token: " + token + " already declared  ")
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
        # print("{0} not found in the symbol table ".format(token))
        return None

    def print(self):
        print(self.symbolTable)
    def symbolTableConstruct(self, p, type):
        ''' 
        SymbolTable is constructed with ply_parser.py 
        For function declaration, function is added to the table with 0 scope
        For variable declaration w definition, variable is added to the symbol table with scope details.
        '''
        if (type == 'varDecl'):
            if (self.ID != '' and self.afterVarAssign):
                self.insert(self.ID, p[1])
                self.ID = ''
                self.afterVarAssign = False
                return
            else:
                self.insert(str(p[2]), str(p[1]))

        if (type == 'funcDecl'):
            ''' 
            If function declaration is encountered then already initiated functionDS is used
            and deleted after it's use to recycle it for the next function declaration.
            '''
            if (self.globalScope == 1):
                if (self.fds.get_name() == 'Unknown'):
                    self.fds.set_name(str(p[2]))
                    self.fds.set_returnType(str(p[1]))
                self.insert(str(p[2]), str(p[1]), self.globalScope - 1)
                self.fds = None
            else:
                print("error: function definition not in a global scope")
                sys.exit(1)

        if (type == 'typeSpecList'):
            '''
            If the typeSpecList is encoutnered from the parser, this type is called. 
            It appends all the arguments of the function. 
            '''
            if (len(p) == 5):
                self.args.append((p[4], p[3]))
            elif (len(p) == 3):
                self.args.append((p[2], p[1]))
            else:
                print("typespec list: unexpected")
                sys.exit(1)
                return
        if (type == 'addMultipleIDs'):
            '''
            If the variables are declared i.e. int a, b, c; then this is called to keep 
            the types of them in check.
            '''
            self.sameIDs.append(str(p[1]))
            return

        if (type == 'beforeCommaList'):
            '''
            This function is called to store the type of multiple identifiers declaration.
            Making use of PLY embedded action.
            '''
            self.sameType = str(p)
            # print('before comma List:   ' + str(p))
            return
        
        if (type == 'afterCommaList'):
            '''
            this function is called after all the IDs are encountered. to insert them into 
            the symbol table with their types and scopes.
            '''
            for id in self.sameIDs:
                self.insert(id, type=self.sameType)
            self.sameIDs.clear()
            self.sameType = ''
            return

    def symbolTable_afterVarAssign(self):
        '''
        This is used when variable is declared with definition. 
        Making use of embedded action
        '''
        self.afterVarAssign = True

    def symbolTable_varAssign(self, ID):
        self.ID = str(ID)
        return

    def inScope(self):
        '''
        Called when the function definition is encountered
        '''
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
        '''
        called when the function RBRACE is encountered
        '''
        if (self.nestedScope != 0b0):
            print("error: missing rbrace")
            sys.exit(1)
        self.globalScope = 1
        return

    def loopInScope(self):
        '''
        called when the loop is encountered. Entering the scope.
        Making use of embedded action
        it performed LSHIFT 1 OR 0b1 on the nestedScope
        '''
        if (self.currentScope == 0):
            # print("error: unexpected loop {0}.{1}".format(p.lineno, p.lexpos))
            print("error: unexpected loop ")
        else:
            self.nestedScope = (self.nestedScope << 1) | 0b1

        return

    def loopOutScope(self):
        '''
        called when you're getting out of the scope. Exiting the scope.
        Making use of embedded action. 
        As mentioned, it performs RSHIFT on nestedScope
        '''
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
        '''
        setting the flag so that every  var-declaration later is a parameter to the function
        '''
        self.functionParam = True

    def endFunctionParam(self):
        '''
        unsetting the flag to know that we're not expecting parameters to the function
        '''
        self.functionParam = False

    def get_fds(self, name):
        '''
        gets function Data-Structure that is maintained for each function.
        '''
        for fds in self.functions:
            E_name = fds.get_name()
            # print(E_name)
            if (E_name == name):
                return fds 
        print('func name not found  ' + name)
        sys.exit(1)

    def getTotalSpace(self, token, scope):
        '''
        This method returns the sum of the memory space required by counting how many 
        variables are in the scope and counting memory of each variable according to their 
        type specifier.
        '''
        token = token.replace(';', '')
        fourByte = ['int', 'unsigned int', 'signed int', 'long', 'float']
        twoByte = ['short', 'unsigned short', 'signed short']
        oneByte = ['bool', 'char', 'signed char', 'unsigned char']
        sum = 0
        for elem in self.symbolTable:
            if ((elem[3] == str(scope))):
                if (elem[2] in fourByte):
                    sum += 4
                elif(elem[2] == twoByte):
                    sum += 2
                elif(elem[2] == oneByte):
                    sum += 1
                else: 
                    sum += 8

        return sum