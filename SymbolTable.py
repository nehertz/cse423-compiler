class SymbolTable:
    
    # We want a dictionary here
    # stores the name, return type
    availableScope = []
    
    def __init__(self):
        self.symbolTable = {}
        self.nestedScope = 0
        # self.nestedScopeDict = {}
        # self.selfScopes = []
        # self.parentScope = 0
        # availableScope.append(0)

    def lookup(self, token):
        if (str(token) in self.symbolTable):
            return self.symbolTable[token]
        else:
            print("error: {0} undeclared".format(token))

    def insert(self, token, type):
        if (str(token) in self.symbolTable):
            print("error: redeclaration of '{0}'")
        else:
            self.symbolTable[str(token)] = str(type)
    # def inScope(self, token, type):
    # def outScope(self, token, type):

    def run(self, lexer):
        for tok in lexer:
            if (str(tok.type) == 'INT'):
                typeStored = 'INT'
                continue

            if (typeStored == 'INT'):
                self.insert(tok.value, typeStored)
                typeStored = ''
                continue
            # if (str(tok.type) == 'LBRACE'):
            #     self.nestedScope += 1
            #     self.
                

    def print(self):
        print("Number of nested Scopes: {}".format(self.nestedScope))
        print(self.symbolTable)
                
