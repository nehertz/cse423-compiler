import sys
import re 
import operator
class BasicRegAlloc:
    def __init__(self, ir):
        self.ir = ir
        ir = ir.replace('\t', '')
        self.funcNameDict = {}
        self.expr = re.compile(r'.*=.*[(\+)|(-)|(\*)|(\|\|)|(&&)|(\^)|(\|)|(&)|(\!)|(<<)|(>>)].*')
        self.divisionExpr = re.compile(r'.*=.*[(\/)|(\%)].*')
        self.assignment = re.compile(r'.*=.*')
        self.functionCall = re.compile(r'.*=.*\(.*\)')
        self.liveVars = {}
        self.lvalues = {}
        self.vertexRegisters = {}
        self.registers = ['%rax','%rcx','%rdx','%rbx','%rsi','%rdi','%r8','%r9','%r10','%r11','%r12','%r13','%r14','%r15']
        self.registersUsage = {}
        self.registersUsage = self.registersUsage.fromkeys(self.registers, 0)
    
    
    def run(self, stReg):
        self.create_dictionary_with_funcName()
        self.analyzeIR()
        self.mapVertex2Register()



    def create_dictionary_with_funcName(self):
        ''' 
        creates a dictionary with the function names as keys
        and scope of the function as a value 
        '''
        funcName = '__initate_first__'
        self.funcNameDict[funcName] = []
        for elem, nextElem in zip(self.ir.split('\n'), self.ir[1:].split('\n')):
            if ('(' in elem and ')' in elem and '{' in nextElem):
                funcName = elem.split('(')
                funcName = funcName[0]
                self.funcNameDict[funcName] = []
                self.funcNameDict[funcName].append(elem)
                # self.funcNameDict[funcName].append(nextElem)
            else:
                self.funcNameDict[funcName].append(elem)
        return
    def analyzeIR(self):
        '''
        Analyzes IR line-by-line using function dictionary. 
        Allocates register for each line depending on variable. 
        Does not make use of liveness, data-flow analysis or anything whatsover.
        Very bad, and going to output long string of assembly code.
        Again very inefficient.
        '''
        for name, scope in self.funcNameDict.items():
            if (name == '__initiate_first__'):
                continue
            for line in scope:
                if ('ret' in line):
                    self.liveVars[line] = '%rax'
                    continue
                elif (self.divisionExpr.match(line)):
                    l = line.split('=')
                    self.lvalues[line] = l[0]
                    l = re.split(r'[(\+)|(-)|(\*)|(\/)|(\%)|(\|\|)|(&&)|(\^)|(\|)|(&)|(\!)|(<<)|(>>)]', l[1])
                    self.liveVars = [l[0], l[1], '%rax', '%rdx']
                    continue
                elif(self.functionCall.match(line)):
                    l = line.split('=')
                    self.liveVars[line] = [l[0]]
                elif (self.expr.match(line)):
                    l = line.split('=')
                    self.lvalues[line] = l[0]
                    l = re.split(r'[(\+)|(-)|(\*)|(\/)|(\%)|(\|\|)|(&&)|(\^)|(\|)|(&)|(\!)|(<<)|(>>)]', l[1])
                    self.liveVars = [l[0], l[1]]
                    continue
                elif(self.assignment.match(line)):
                    l = line.split('=')
                    self.liveVars[line] = [l[1]]
        return
    
    def mapVertex2Register(self):
        for key, value in self.funcNameDict.items():
            if (key == '__initiate_first__'):
                continue
            for line in value:
                self.insertVertexRegisters(line)
                    
                    # if ('%r' in elem):
                    #     self.vertexRegisters[elem] = elem
                    #     self.registersUsage[elem] += 1
                    #     continue
                    # self.insertVertexRegisters(elem)
        return

    def insertVertexRegisters(self, line):
        regs = ['%rax','%rcx','%rdx','%rbx','%rsi','%rdi','%r8','%r9','%r10','%r11','%r12','%r13','%r14','%r15']
        
        self.vertexRegisters[line] = []

        for elem in line:
            if ('%r' in elem):
                # self.vertexRegisters[line] = []
                self.vertexRegisters[line].append(elem)
                regs.remove(elem)
                continue
            min_reg = min(self.registersUsage.items(), key = operator.itemgetter(1))[0]
            self.vertexRegisters[line].append(min_reg)
            self.registersUsage[min_reg] += 1
        
        # if (var in self.vertexRegisters):
            # return 
        # min_reg = min(self.registersUsage.items(), key = operator.itemgetter(1))[0]
        # self.vertexRegisters[var] = min_reg 
        # self.registersUsage[min_reg] += 1
        return

    def getVertexRegisters(self, line, var):
        for elem, reg in zip(line, self.vertexRegisters[line]):
            if (elem == var):
                return reg
        print('Error: register not allocated for ' + str(var))
        print('statement: ' + line)
        sys.exit(1)
