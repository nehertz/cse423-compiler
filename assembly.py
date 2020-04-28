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
            
            #TODO self.setReg.movFromMem2Reg(str(RHS))
            self.ass.append(["mov", self.getMemLocation(RHS), "%eax"])
            self.ass.append(["mov", "%eax", self.getMemLocation(LHS)])
            self.ass.append(["mov", "$0", "%eax"])
        return
    
    def simpleArithmetic(self, statement):
        ops = statement[3]
        if (ops == '+' or ops == '-'):
            self.plusAndMinus(statement[0], statement[2], statement[4], ops)
        elif (ops == '*'):
            self.times(statement[0], statement[2], statement[4])
        elif (ops == '/'):
            self.divide(statement[0], statement[2], statement[4])
        elif (ops == '%'):
            self.modulo(statement[0], statement[2], statement[4])
        else:
            print('unknow ops\n')
            exit()


    def plusAndMinus(self, LHS, RHS1, RHS2, ops):
        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)

        # RHS1 = constant &&  RHS2 = constant
        if (constFlag1 and constFlag2):
            if (ops == '+'):
                result = RHS1 + RHS2
            elif (ops == '-'):
                result = RHS1 - RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])
        
        # RHS1 = constant &&  RHS2 = var
        elif (constFlag1 and not constFlag2):
            # mov <RHS2> <reg1>
            instruction = self.setReg.movFromMem2Reg(RHS2)
            reges = instruction.split(" ")[2].strip()
            self.ass.append([instruction.strip()])
            # add <const>,<reg1> or sub 
            if (ops == '+'):
                self.ass.append(["add", "$"+str(RHS1) , reges])
            elif (ops == '-'):
                self.ass.append(["sub", "$"+str(RHS1) , reges])
            # mov <reg1>, <LHS>
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        # RHS1 = var && RHS2 = constant
        elif (not constFlag1 and constFlag2):
            # mov <RHS1> <reg1>
            instruction = self.setReg.movFromMem2Reg(RHS1)
            reges = instruction.split(" ")[2].strip()
            self.ass.append([instruction.strip()])
            # add <const>,<reg1>
            if (ops == '+'):
                self.ass.append(["add", "$"+str(RHS2) , reges])
            elif (ops == '-'):
                self.ass.append(["sub", "$"+str(RHS2) , reges])
             # mov <reg1>, <LHS>
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        # RHS1 = var && RHS2 = var 
        elif (not constFlag1 and not constFlag2):
            # mov <RHS1> <reg1>
            instruction = self.setReg.movFromMem2Reg(RHS1)
            reges = instruction.split(" ")[2].strip()
            self.ass.append([instruction.strip()])
            # add <RHS2>,<reg1>`
            if (ops == '+'):
                self.ass.append(["add", self.getMemLocation(RHS2) , reges])
            elif (ops == '-'):
                self.ass.append(["sub", self.getMemLocation(RHS2) , reges])
            # mov <reg1>, <LHS>
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])


    def times(self, LHS, RHS1, RHS2):
        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)
        
        if (constFlag1 and constFlag2):
            result = RHS1 * RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])

        # this is the case where a constant times a varaible
        elif (constFlag1 and not constFlag2):
            # mov RHS1 LHS
            self.ass.append(["mov", "$"+str(RHS1) , self.getMemLocation(LHS)])
            # mov RHS2 reg1
            instruction = self.setReg.movFromMem2Reg(RHS2)
            reges = instruction.split(" ")[2].strip()
            self.ass.append([instruction.strip()])
            # imul LHS reg1
            self.ass.append(["imul", self.getMemLocation(LHS) , reges])
            # mov reg1 LHS 
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        elif (not constFlag1 and constFlag2):
            # mov RHS2 LHS
            self.ass.append(["mov", "$"+str(RHS2) , self.getMemLocation(LHS)])
            # mov RHS1 reg1
            instruction = self.setReg.movFromMem2Reg(RHS1)
            reges = instruction.split(" ")[2].strip()
            self.ass.append([instruction.strip()])
            # imul LHS reg1
            self.ass.append(["imul", self.getMemLocation(LHS) , reges])
            # mov reg1 LHS 
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        elif (not constFlag1 and not constFlag2):
            # mov RHS1 reg1 
            instruction = self.setReg.movFromMem2Reg(RHS1)
            reges = instruction.split(" ")[2].strip()
            self.ass.append([instruction.strip()])
            # imul RHS2 reg1
            self.ass.append(["imul", self.getMemLocation(RHS2) , reges])
            # mov reg1 LHS
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])
        

    #  - `add <reg>,<reg>`
    # - `add <reg>,<mem>`
    # - `add <mem>,<reg>`
    # - `add <const>,<reg>`
    # - `add <const>,<mem>`

    #     - Destination must be a register
    # - `imul <reg32>,<reg32>`
    # - `imul <mem>,<reg32>`
    def divide(self, LHS, RHS1, RHS2):
        pass

    def modulo(self, LHS, RHS1, RHS2):
        pass


    def determineConstant(self, RHS1, RHS2):
        constFlag1 = 0
        constFlag2 = 0
        floatPatten = re.compile(r"[0-9]+\.[0-9]+")
        intPatten = re.compile(r"^[-+]?\d+$")

        if (intPatten.match(RHS1)):
            RHS1 = int(RHS1)
            constFlag1 = 1
        elif (floatPatten.match(RHS1)):
            RHS1 = float(RHS1)
            constFlag1 = 1
        
        if (intPatten.match(RHS2)):
            RHS2 = int(RHS2)
            constFlag2 = 1
        elif (floatPatten.match(RHS2)):
            RHS2 = float(RHS2)
            constFlag2 = 1

        return constFlag1, constFlag2, RHS1, RHS2

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


    