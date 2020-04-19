class functionDS:
    def __init__(self, name):
        self.funcName = name 
        self.vars = []
        self.returnType = None
    
    def add_vars_type(self, typeName):
        self.vars.append(typeName)
    
    def get_vars_type(self):
        return self.vars
    
    def print(self):
        print('function name: ' + self.funcName)
        print('vars Types List ' )
        print(self.vars)
        
    def get_name(self):
        return self.funcName
    
    def set_name(self, name):
        self.funcName = name
    
    def get_argc(self):
        return len(self.vars)

    def set_returnType(self, name):
        self.returnType = name