class SymbolTable:
    
    # We want a dictionary here
    # stores the name, return type
    
    def __init__(self):
        self.symbolTable = {}
        self.nestedScope = 0
        self.nestedScopeDict = {}
        self.selfScopes = []
        self.parentScope = None
        self.currentScope = 0
        self.globalScope = False

    # def lookup(self, token):
    #     if (str(token) in self.symbolTable):
    #         return self.symbolTable[token]
    #     else:
    #         print("error: {0} undeclared".format(token))

    def insert(self, token, type):
        if (str(token) in self.symbolTable):
            print("error: redeclaration of '{0}'")
        else:
            self.symbolTable[str(token)] = str(type)
    # def inScope(self, token, type):
    # def outScope(self, token, type):

    def print(self):
        print("Number of nested Scopes: {}".format(self.nestedScope))
        print(self.symbolTable) 


    def run(self, lexer):
        for tok in lexer:
            if (str(tok.type) == 'INT'):
                typeStored = 'INT'
                continue

            if (typeStored == 'INT'):
                self.insert(tok.value, typeStored)
                typeStored = ''
                continue
            # LBRACE means new scope encountered
            # increase the nested scope, and add that to the 1
            # selfScope is a stack like list which is used to find the current 
            # scope and only add variables to it.
            if (str(tok.type) == 'LBRACE'):
                self.nestedScope += 1
                self.selfScopes.append(self.nestedScope)
                self.symbolTable[self.nestedScope] = SymbolTable()
                self.st = self.symbolTable[self.nestedScope]
                self.st.parentScope = self
                # self.currentScope = self.selfScopes[len(self.selfScopes) - 1]
                len(self.selfScopes)
            if (str(tok.type) == 'RBRACE'):
                self.selfScopes.pop()
                # self.currentScope = self.selfScopes[len(self.selfScopes) - 1]
                len(self.selfScopes)

    def lookup(self, token):
        if (str(token) in self.symbolTable):
            return self.symbolTable[token]
        else:
            return self.lookupParent(token)
    
    def lookupParent(self, token):
        if (str(token) in self.symbolTable):
            return self.symbolTable[token]
        elif (not self.globalScope):
            return self.lookupParent(token)
        else:
            print("error: {0} undeclared".format(token))
            return None