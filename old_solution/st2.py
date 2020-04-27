class SymbolTable:

        def __init__(self, id=0):
            self.symbolTable = {}
            self.scopes = 0
            self.scopesList = []
            self.id = id
        def lookup(self, token):
            if (str(token) in self.symbolTable):
                return self.symbolTable[token]
            else:
                print("error: {0} undeclared".format(token))
                return None

        def insert(self, token, type):
            if (str(token) in self.s):
                print("error: redeclaration of '{0}'".format(token))
            else:
                self.symbolTable(str(token))
        def run(self, lexer):
            inScope = 0b0
            for tok in lexer:
                typeStored = self.checkTypes(tok)
                if (typeStored == ''):
                    continue
                if (typeStored == 'INT'):
                    self.insert(tok.value, typeStored)
                    typeStored = ''
                    continue
                
                if(str(tok.type) == 'LBRACE'):
                    inScope = (inScope << 1) | 0b1
                    self.scopes += 1
                    st = subTable()
                    self.symbolTable[self.scopesList] = st
                    self.scopesList.append(scopes)

                if (inScope == 0b0):
                    if (str(tok.type) == 'RBRACE'):
                        inScope = (inScope >> 1)
                        self.scopesList.pop()
                        self.scopes -= 1
                    else:
                        self.symbolTable[self.scopesList(len(self.scopesList))] 

        
        def checkTypes(self, tok):
            if (str(tok.type) == 'INT'):
                return 'INT'
            return ''
                        
                    
                



        class subTable():
                def __init__(self):
                        self.symbolTable = {}
                 
                def lookup(self, token):
                    if (str(token) in self.symbolTable):
                        return self.symbolTable[token]
                    else:
                        print("error: {0} undeclared".format(token))
                        return None
            
                def insert(self, token, type):
                    if (str(token) in self.symbolTable):
                        print("error: redeclaration of '{0}'")
                    else:
                        self.symbolTable[str(token)] = str(type)