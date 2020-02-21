class SymbolTable:
        def __init__(self):
                self.symbolTable = []
                self.currentScope = 0
                self.nestedScope = 0b0

        def run(self, lexer):
                for tok in lexer:
                        if (str(tok.type) == 'INT'):
                                typeStored = 'INT'
                                continue
                        if (typeStored == 'INT'):
                                self.insert(tok.value, typeStored)
                                typeStored = ''
                                continue

                        if (typeStored == '' and str(tok.type) == 'ID'):
                                self.lookup(tok.value)

                        if (str(tok.type) == 'LBRACE'):
                                if (self.nestedScope == 0b0):
                                        self.currentScope += 1
                                else:
                                        self.nestedScope = (self.nestedScope << 1) | 0b1
                        elif (str(tok.type) == 'RBRACE'):
                                if (self.nestedScope != 0b0):
                                        self.nestedScope >>= 1

        def insert(self, token, type):
                if (self.nestedScope == 0b0 and self.currentScope == 0):
                        self.symbolTable.append((token, type, str(self.currentScope)))
                
                scope = str(self.currentScope) + str(self.nestedScope)
                self.symbolTable.append((token, type, scope))

        def lookup(self, token):
                # scope = str(self.currentScope) + str(self.nestedScope) 
                self.lookupInternal(token, self.currentScope, self.nestedScope)
        
        def lookupInternal(self, token, curr_scope, nested_scope):
                if (nested_scope != 0b0):
                        ans = self.find(token, str(curr_scope) + str(nested_scope))
                        if (ans[0] == False):
                                nested_scope >>= 1
                                self.lookupInternal(token, curr_scope, nested_scope)
                        else: 
                                return ans[1]
                else:
                        ans = self.find(token, str(curr_scope) + str(nested_scope))
                        if (ans[0] == True):
                                return ans[1]
                        else:
                                # search in global scope then
                                ans = self.find(token, str(0))
                                if (ans[0]):
                                        print("error: {0} token undeclared".format(token))
                                        return None
                                
                                else:
                                        return ans[1]


        def find(self, token, scope):
                for elem in self.symbolTable:
                        if (elem[2] == scope):
                                if (elem[0] == token):
                                        return (True, elem[1])
                                else: 
                                        continue
                        else:
                                continue 
                return (False, None)
        
        def print(self):
                print(self.symbolTable)