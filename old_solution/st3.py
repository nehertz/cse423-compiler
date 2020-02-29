class SymbolTable():

        def __init__(self):
                self.parents = []
                self.symbolTable = {}
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
                
