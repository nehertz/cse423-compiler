'''
Basic Register Allocation:
This algorithm goes over IR, line-by-line and fetches the live-variables of that line
and assigns them the registers. The only efficient thing it takes care of is that it
utilizes the lowest used-registers first and makes it kind of uniform strain on all 
of the available registers.
'''


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
                    self.liveVars[line] = ['%rax']
                    continue
                elif (self.divisionExpr.match(line)):
                    l = line.split('=')
                    self.lvalues[line] = l[0]
                    l = re.split(r'[(\+)|(-)|(\*)|(\/)|(\%)|(\|\|)|(&&)|(\^)|(\|)|(&)|(\!)|(<<)|(>>)]', l[1])
                    self.liveVars[line] = [l[0], l[1], '%rax', '%rdx', self.lvalues[line]]
                    continue
                elif(self.functionCall.match(line)):
                    l = line.split('=')
                    self.liveVars[line] = [l[0]]
                elif (self.expr.match(line)):
                    l = line.split('=')
                    self.lvalues[line] = l[0]
                    l = re.split(r'[(\+)|(-)|(\*)|(\/)|(\%)|(\|\|)|(&&)|(\^)|(\|)|(&)|(\!)|(<<)|(>>)]', l[1])
                    self.liveVars[line] = [l[0], l[1], self.lvalues[line]]
                    continue
                elif(self.assignment.match(line)):
                    l = line.split('=')
                    self.liveVars[line] = [l[1], l[0]]
        return
    
    def mapVertex2Register(self):
        '''
        After all the live-variables stored, we go to line-by-line 
        and give each variable from that line a register
        '''
        for key, value in self.funcNameDict.items():
            if (key == '__initiate_first__'):
                continue
            for line in value:
                self.insertVertexRegisters(line)
        return

    def insertVertexRegisters(self, line):
        '''
        After 
        '''
        regs = ['%rax','%rcx','%rdx','%rbx','%rsi','%rdi','%r8','%r9','%r10','%r11','%r12','%r13','%r14','%r15']
        
        self.vertexRegisters[line] = []

        for elem in line:
            if ('%r' in elem):
                self.vertexRegisters[line].append(elem)
                regs.remove(elem)
                continue
            min_reg = min(self.registersUsage.items(), key = operator.itemgetter(1))[0]
            self.vertexRegisters[line].append(min_reg)
            self.registersUsage[min_reg] += 1
        return

    def getVertexRegisters(self, line, var):
        # for e
        line2 = ''.join(elem for elem in line)     
        
        for elem, reg in zip(line, self.vertexRegisters[line2]):
            if (elem == var):
                return reg
        print('Error: register not allocated for ' + str(var))
        print('statement: ' + line)
        sys.exit(1)
