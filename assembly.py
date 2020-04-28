from ply_scanner import assignment
from ply_scanner import arithmetic
import re

class assembly:
    def __init__(self, ir, ig, setReg):
        self.IR = ir
        self.ass = []
        self.ig = ig
        self.setReg = setReg
        self.symbolTable = {}

    def run(self):
        lineNumber = 0
        funcScope = []
        flag = 0

        self.ig.run(self.setReg)

        for line in self.IR:
            # translate function name and args to assembly 
            if ('(' in line and ')' in line and self.IR[lineNumber+1][0] == '{'):
                self.funcName(line)

            # translate function statement body to assembly 
            elif ('{' in line):
                flag = 1
                lineNumber += 1
                continue
            elif ('}' in line):
                flag = 0
                self.funcBody(funcScope)
                funcScope = []
            elif (flag):
                funcScope.append(line)

            lineNumber += 1
            
        self.printAssembly()
    
    def funcName(self, line):
        # creates function label, creates assembly code to handel args if exist. 
        self.ass.append(["_" + line[0]])
    

    def funcBody(self, body):
        self.symbolTable = {}
        
        self.stackInitial(body)

        # scanning through the body, 
        for statement in body:
            # translates the function call. 
            if ('(' in statement and ')' in statement):
                self.funcCall(statement)    

             # translate assignment statement 
            elif (len(statement) >= 3 and statement[1] in assignment):
                self.assignment(statement)
            
            # simply creates the goto and label code
            elif ('goto' in statement):
                self.goto(statement)

            # not sure about this part -.- 
            elif ('if' in statement):
                self.conditional(statement)

    # initialize the stack, create initial space on the stack for local variables
    def stackInitial(self, body):
        stackSize = 4
        tempCode = []
        tempCode.append(["push", "%ebp"])
        tempCode.append(["mov", "esp", "ebp"])
        for statement in body:
            stackLocation = "-" + str(stackSize) + "(%ebp)"
            if(len(statement) == 1 and ":" not in statement[0] and (statement[0] not in self.symbolTable.keys())):
                dict = {statement[0] : stackLocation}
                self.symbolTable.update(dict)
                stackSize += 4
                self.setReg.insertMemory(statement[0], stackLocation)

            elif(len(statement) >= 3 and statement[1] == '=' and (statement[0] not in self.symbolTable.keys()) and ":" not in statement[0]):
                dict = {statement[0] : stackLocation}
                self.symbolTable.update(dict)
                stackSize += 4
                self.setReg.insertMemory(statement[0], stackLocation)

        tempCode.append(["sub", "$" + str(stackSize), "esp"])
        # print(self.symbolTable)
        for itme in tempCode:
            self.ass.append(itme)

    # Takes variable name as input, returns its corresponding mem location
    # return will be something like -4(%ebp)
    def getMemLocation(self, var):
        if(var not in self.symbolTable):
            print("var not on the stack")
        else:
            return self.symbolTable[var]
    

    def assignment(self, statement):
        # Assignment should handles simple assignment like a = 1
        # and assignment with arithmetic, a = 1 + b
        # One special case: function call in arithmetic. 
        if (len(statement) == 3 ):
            self.simpleAssign(statement[0], statement[2])

        elif (statement[3] in arithmetic):
            self.simpleArithmetic(statement)
    
    def simpleAssign(self, LHS, RHS):
        floatPatten = re.compile(r"[0-9]+\.[0-9]+")
        intPatten = re.compile(r"^[-+]?\d+$")
        # assignment like a = 2 will be translate to 'mov $2 a_location'
        if (intPatten.match(RHS) or floatPatten.match(RHS)):
            RHS = "$" + str(RHS)
            LHS = self.getMemLocation(LHS)
            self.ass.append(["mov", RHS, LHS])

        # assignment like a = b will be tranlate to:
        # mov b_location %eax
        # mov %eax a_location
        # mov $0 %eax 
        else:
            self.ass.append(["mov", self.getMemLocation(RHS), "%eax"])
            self.ass.append(["mov", "%eax", self.getMemLocation(LHS)])
            self.ass.append(["mov", "$0", "%eax"])
        return
    
    def simpleArithmetic(self, statement):
        ops = statement[3]
        if (ops == '+'):
            self.plus(statement[0], statement[2], statement[4])
        elif (ops == '-'):
            self.minus(statement[0], statement[2], statement[4])
        elif (ops == '*'):
            self.times(statement[0], statement[2], statement[4])
        elif (ops == '/'):
            self.divide(statement[0], statement[2], statement[4])
        elif (ops == '%'):
            self.modulo(statement[0], statement[2], statement[4])
        else:
            print('unknow ops\n')
            exit()

    def plus(self, LHS, RHS1, RHS2):
        pass

    def minus(self, LHS, RHS1, RHS2):
        pass

    def times(self, LHS, RHS1, RHS2):
        pass

    def divide(self, LHS, RHS1, RHS2):
        pass

    def modulo(self, LHS, RHS1, RHS2):
        pass

    def goto(self, statement):
        pass

    def funcCall(self, statement):
        pass
    

    def printAssembly(self):
        str1 = " "
        indentFlag = 0
        for list in self.ass:
            if(len(list) == 1 and list[0][0] == '_'):
                print(list[0])
            else:
                print('\t', str1.join(list))


    