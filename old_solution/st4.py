import sys
class SymbolTable:
        def __init__(self):
                self.symbolTable = []
                self.currentScope = 0
                self.nestedScope = 0b0

        # def run(self, lexer):
        #         isFunction = False
        #         for tok in lexer:
        #                 if (str(tok.type) == 'INT'):
        #                         typeStored = 'INT'
        #                         continue
        #                 if (typeStored == 'INT'):
        #                         self.insert(tok.value, typeStored)
        #                         isFunction = True
        #                         typeStored = ''
        #                         continue
        #                 if (isFunction):
        #                         if (tok.type == 'LPAREN'):
        #                                 if (self.currentScope == 0b0):
        #                                         self.currentScope += 1
        #                                         continue
        #                                 else:
        #                                         # Todo: print line numbers
        #                                         print("error: function {0} declaration can't be inside any scope {1}:{2}".format(tok.value, tok.lineno, tok.lexpos))
        #                                         sys.exit(1)
        #                         if (tok.type == 'RPAREN'):
        #                                 isFunction = False
        #                                 continue

        #                 if (typeStored == '' and str(tok.type) == 'ID'):
        #                         self.lookup(tok)
        #                         continue

        #                 if (str(tok.type) == 'LBRACE'):
        #                         if (isFunction):
        #                                 continue
        #                         # if (self.nestedScope == 0b0):
        #                         #         self.currentScope += 1
        #                         #         continue
        #                         # else:
        #                         self.nestedScope = (self.nestedScope << 1) | 0b1
        #                         continue
        #                 elif (str(tok.type) == 'RBRACE'):
        #                         if (isFunction and self.nestedScope == 0b0):
        #                                 isFunction = False
        #                                 self.currentScope -= 1
        #                                 continue
        #                         if (self.nestedScope != 0b0):
        #                                 self.nestedScope >>= 1
        #                                 continue
        #                         else:
        #                                 self.currentScope -= 1
        #                                 continue

        def insert(self, token, type):
                if (self.nestedScope == 0b0 and self.currentScope == 0):
                        self.symbolTable.append((token, type, str(self.currentScope)))
                        return
                
                scope = str(self.currentScope) + str(self.nestedScope)
                self.symbolTable.append((token, type, scope))

        def lookup(self, token):
                # scope = str(self.currentScope) + str(self.nestedScope) 
                self.lookupInternal(token, self.currentScope, self.nestedScope)
        
        def lookupInternal(self, token, curr_scope, nested_scope):
                if (nested_scope != 0b0):
                        ans = self.find(token.value, str(curr_scope) + str(nested_scope))
                        if (ans[0] == False):
                                nested_scope >>= 1
                                self.lookupInternal(token.value, curr_scope, nested_scope)
                        else: 
                                return ans[1]
                else:
                        ans = self.find(token.value, str(curr_scope) + str(nested_scope))
                        if (ans[0] == True):
                                return ans[1]
                        else:
                                # search in global scope then
                                ans = self.find(token.value, str(0))
                                if (not ans[0]):
                                        print("error: {0} token undeclared. Current scope: {1}".format(token, self.currentScope))
                                        sys.exit(1)
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