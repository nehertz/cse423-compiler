class functionDS:
    def __init__(self, name):
        self.funcName = name 
        self.vars = []
    
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