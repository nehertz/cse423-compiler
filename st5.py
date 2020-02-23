import sys
class SymbolTable:
        def __init__(self):
                self.symbolTable = []
                self.currentScope = 0
                self.globalScope = 0
                self.nestedScope = 0b0
                self.args = []
                self.ID = ''

        def insert(self, token, type, scope=-1):
                if (scope == -1):
                        if (self.nestedScope == 0b0):
                                self.symbolTable.append((token, type, str(self.currentScope)))
                        else:
                                self.symbolTable.append((token, type, str(self.currentScope) + str(self.nestedScope)))
                else:
                        self.symbolTable.append((token, type, scope))

        def lookup(self, token):
                # scope = str(self.currentScope) + str(self.nestedScope) 
                return
        def print(self):
                print(self.symbolTable)
        # TODO: var-assign with declaration not supported
        def symbolTableConstruct(self, p, type):
                if (type == 'varDecl'):
                        if (len(p) == 3):
                                if (self.ID != ''):
                                        print("in if var decl: ID: {0}  type: {1}".format(self.ID, p[1]))
                                        self.insert(self.ID, p[1])
                                        self.ID = ''
                                        return
                                
                                print("var decl: ID: {0}  type: {1}".format(p[2], p[1]))
                                self.insert(str(p[2]), str(p[1]))

                                
                        else:
                                print("currently not supporting")

                if (type == 'funcDecl'):
                        if (self.globalScope == 1):
                                self.insert(str(p[1]), str(p[2]), self.globalScope - 1)
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
                                return
                



        def symbolTable_varAssign(self, ID):
                self.ID = ID
                return
        def inScope(self):
                self.currentScope += 1
                self.globalScope = 0
                if (len(self.args) != 0):
                        for elem in self.args:
                                # self.symbolTable.append(elem[0], elem[1])
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
                else :
                        self.nestedScope = (self.nestedScope << 1) | 0b1
                        
                return 
        def loopOutScope(self):
                if (self.nestedScope == 0b0):
                        print("error: No matching left brace found")
                else:
                        self.nestedScope >>= 1
                return   

