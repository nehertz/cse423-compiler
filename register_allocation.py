import re
class interference_graph:
    def __init__(self, ir):
        self.ir = []
        self.tmpIR = ir
        # self.func = re.compile(r'^[\w\d]+[\w\d]*\(.*\)')
        # self.Lbrace = re.compile(r'\{')
        # self.Rbrace = re.compile(r'\}')
        self.expr = re.compile(r'.*=.*')
        self.readIR(self.tmpIR)
        self.liveVars = {}
        self.funcNameDict = {}

    def create_dictionary_with_funcName(self):
        ''' 
        creates a dictionary with the function names as keys
        and scope of the function as a value 
        '''
        funcName = '__initate_first__'
        for elem, nextElem in zip(self.ir, self.ir[1:]):
            if ('(' in elem and ')' in elem and '{' in nextElem):
                funcName = elem.split('(')
                funcName = funcName[0]
                self.funcNameDict[funcName] = []
                self.funcNameDict[funcName].append(elem)
                # self.funcNameDict[funcName].append(nextElem)
            else:
                self.funcNameDict[funcName].append(elem)
        return
    # variable is live at a particular point in the program if its 
    # value at that point will be used in the future (dead, otherwise)
    def test_live(self):
        for key, val in self.funcNameDict:
            if (key == '__initiate_first__'):
                continue 
            else:
                for line in reversed(val[1:]):
                    if (self.expr.match(line)):
                        

                    


    
    def run(self):
        for line in self.ir:
            if (self.expr.match(line)):
                

                


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def readIR(self, fileString):
        fileString = [x.strip() for x in fileString]  
        fileString = [x.replace('\t', ' ') for x in fileString]  
        for line in fileString:
            list = line.split()
            self.ir.append(list)
