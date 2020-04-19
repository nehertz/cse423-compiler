from SymbolTable import SymbolTable

class childST(SymbolTable):
    def __init__(self):
        super().__init__()
            self.currentScope = 0
            self.globalScope = False
    
    
    # def run(self, lexer):
    #     for tok in lexer:
    #         if (str(tok.type) == 'INT'):
    #             typeStored = 'INT'
    #             continue

    #         if (typeStored == 'INT'):
    #             self.insert(tok.value, typeStored)
    #             typeStored = ''
    #             continue
    #         # LBRACE means new scope encountered
    #         # increase the nested scope, and add that to the selfScope
    #         # selfScope is a stack like list which is used to find the current 
    #         # scope and only add variables to it.
    #         if (str(tok.type) == 'LBRACE'):
    #             self.nestedScope += 1
    #             self.selfScopes.append(self.nestedScope)
    #             self.symbolTable[self.nestedScope] = SymbolTable()
    #             self.st = self.symbolTable[self.nestedScope]
    #             self.st.parentScope = self
    #             self.currentScope = self.selfScopes[len(self.selfScopes) - 1]
            
    #         if (str(tok.type) == 'RBRACE'):
    #             self.selfScopes.pop()
    #             self.currentScope = self.selfScopes[len(self.selfScopes) - 1]
    
    # def lookup(self, token):
    #     if (str(token) in self.symbolTable):
    #         return self.symbolTable[token]
    #     else:
    #         typeFound = self.lookupParent(token):
    #         return None
    
    
    # def lookupParent(self, token):
    #     if (str(token) in self.symbolTable):
    #         return self.symbolTable[token]
    #     elif (not self.globalScope):
    #         return self.lookupParent(self, token)
    #     else:
    #         print("error: {0} undeclared".format(token))
    #         return None


            
            
            
