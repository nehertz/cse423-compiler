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
        self.st = self

    # def lookup(self, token):
    #     if (str(token) in self.symbolTable):
    #         return self.symbolTable[token]
    #     else:
    #         print("error: {0} undeclared".format(token))

    def insert(self, token, type):
        if (str(token) in self.symbolTable):
            print("error: redeclaration of '{0}'".format(token))
        else:
            self.symbolTable[str(token)] = str(type)
    # def inScope(self, token, type):
    # def outScope(self, token, type):

    def print(self):
        print("Number of nested Scopes: {}".format(self.nestedScope))
        for i in range(1, self.nestedScope + 1):
            print(self.symbolTable[i].print2())
        print(self.symbolTable)

    def print2(self):
        return self.symbolTable


    def run(self, lexer):
        for tok in lexer:
            if (str(tok.type) == 'INT'):
                typeStored = 'INT'
                continue

            if (typeStored == 'INT'):
                self.st.insert(tok.value, typeStored)
                typeStored = ''
                continue

            if (typeStored == '' and str(tok.type) == 'ID'):
                self.st.lookup(tok)
            # LBRACE means new scope encountered
            # increase the nested scope, and add that to the 1
            # selfScope is a stack like list which is used to find the current 
            # scope and only add variables to it.
            if (str(tok.type) == 'LBRACE'):
                self.st.nestedScope += 1
                self.st.selfScopes.append(self.nestedScope)
                self.st.symbolTable[self.nestedScope] = SymbolTable()
                self.st = self.symbolTable[self.nestedScope]
                self.st.parentScope = self
                # self.currentScope = self.selfScopes[len(self.selfScopes) - 1]
                len(self.selfScopes)
            if (str(tok.type) == 'RBRACE'):
                # self.st.selfScopes.pop()
                # self.currentScope = self.selfScopes[len(self.selfScopes) - 1]
                self.st = self.parentScope
                # len(self.st.selfScopes)

    def lookup(self, token):
        if (str(token.value) in self.symbolTable):
            return self.symbolTable[token.value]
        else:
            return self.lookupParent(token)
    
    def lookupParent(self, token):
        if (str(token.value) in self.symbolTable):
            return self.symbolTable[token.value]
        elif (not self.globalScope):
            return self.parentScope.lookupParent(token)
        else:
            print("error: {0} undeclared".format(token))
            return None