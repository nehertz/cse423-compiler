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
        self.interferenceGraph = {}
        self.num = re.compile(r'\d+')
        self.EdgesList = []
        self.VertexList = []

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
    #TODO: Check if the lvalue is also live. 
    #TODO: Check for mov instructions for IG.
    def test_live(self):
        for key, val in self.funcNameDict:
            if (key == '__initiate_first__'):
                continue 
            else:
                for line in reversed(val[1:]):
                    if (self.expr.match(line)):
                        (lvalue, rvalue1, rvalue2) = self.checkLiveness(line)
                        self.insertNodeIG(lvalue)
                        if (self.num.match(rvalue1)):
                            if (self.num.match(rvalue2)):
                                self.liveVars[line] = [lvalue]
                                pass
                            else:
                                self.liveVars[line] = [rvalue2, lvalue]
                                self.insertNodeIG(rvalue2)
                        else:

                            if (self.num.match(rvalue2)):
                                self.liveVars[line] = [rvalue1, lvalue]
                                self.insertNodeIG(rvalue1)
                            else:
                                self.liveVars[line] = [rvalue1, rvalue2, lvalue]
                                self.insertNodeIG(rvalue1)
                                self.insertNodeIG(rvalue2)
                for line,nextLine in zip(val[1:], val[2:]):
                    if (line in self.liveVars and nextLine in self.liveVars):
                        self.liveVars[line] = self.checkLiveVarsInNextLine(self.liveVars[line], self.liveVars[nextLine])

        return


    def checkLiveVarsInNextLine(self, vars, varsNextLine):
        lvalue = vars[-1]
        vars.remove(lvalue)
        for elem in varsNextLine:
            if (elem == varsNextLine[-1]):
                continue 
            if (elem != lvalue):
                vars.insert(0, elem)
        return vars            
    
    def checkLiveness(self, line):
        line = line.split('=')
        var1 = line[0]
        line = line[1]
        line = re.split(r'[\/\+\-\*\%]', line)
        return (var1, line[0], line[1])

    def insertNodeIG(self, val):
        if (not val in self.interferenceGraph):
            self.interferenceGraph[val] = []
        return
                
    def readIR(self, fileString):
        fileString = [x.strip() for x in fileString]  
        fileString = [x.replace('\t', ' ') for x in fileString]  
        for line in fileString:
            list = line.split()
            self.ir.append(list)

    def initiateInterferenceGraph(self):
        self.interferenceGraph['%rax'] = []
        self.interferenceGraph['%rcx'] = []
        self.interferenceGraph['%rdx'] = []
        self.interferenceGraph['%rbx'] = []
        self.interferenceGraph['%rsi'] = []
        self.interferenceGraph['%rdi'] = []
        self.interferenceGraph['%rsp'] = []
        self.interferenceGraph['%rbp'] = []
        self.interferenceGraph['%r8'] = []
        self.interferenceGraph['%r9'] = []
        self.interferenceGraph['%r10'] = []
        self.interferenceGraph['%r11'] = []
        self.interferenceGraph['%r12'] = []
        self.interferenceGraph['%r13'] = []
        self.interferenceGraph['%r14'] = []
        self.interferenceGraph['%r15'] = []

    
    def createEdgesList(self):
        for key, value in self.interferenceGraph.items():
            if (value):
                for elem in value:
                    self.EdgesList.append((key, elem))
        return
    def createVertexList(self):
        for key, _ in self.interferenceGraph.items():
            if (key not in self.VertexList):
                self.VertexList.append(key)
        return

