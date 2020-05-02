from ply_scanner import assignment
from ply_scanner import arithmetic
from ply_scanner import logical
import re
import sys

class assembly2:
    def __init__(self, ir, ig, setReg):
        self.IR = ir
        self.ass = []
        self.ig = ig
        self.setReg = setReg
        self.symbolTable = {}
        self.stackSize = 8
        self.floatPatten = re.compile(r"[0-9]+\.[0-9]+")
        self.intPatten = re.compile(r"^[-+]?\d+$")

    def run(self):
        lineNumber = 0
        funcScope = []
        flag = 0
        name = ""
        paramCount = 0
        self.ig.run(self.setReg)
        for line in self.IR:
            # translate function name to assembly 
            if ('(' in line and ')' in line and self.IR[lineNumber+1][0] == '{'):
                name, paramCount = self.funcName(line)
            # translate function statement body to assembly 
            elif ('{' in line):
                flag = 1
                lineNumber += 1
                continue
            elif ('}' in line):
                flag = 0
                self.funcBody(funcScope, name, paramCount)
                funcScope = []
            elif (flag):
                funcScope.append(line)
            lineNumber += 1
        self.printAssembly()
    
    def funcName(self, line):
        # creates function label, creates assembly code to handel args if exist. 
        self.ass.append(["_" + line[0]])
        paramCount = []
        for item in line:
            if ("(" not in item and ")" not in item and "," not in item and item != line[0]):
               paramCount.append(item)
        return "_" + line[0], paramCount

    def funcBody(self, body, name, paramCount):

        self.symbolTable = {}
        self.stackSize = 8
       
        self.stackInitial(body, paramCount)
        flag = 1
        mainFlag = 1
       
        if ('_main' not in name):
            instructions =self.setReg.calleeSavedReg()
            self.ass.append([instructions.split("\n")[0]])
            self.ass.append([instructions.split("\n")[1]])
            self.ass.append([instructions.split("\n")[2]])
            mainFlag = 0 

        # scanning through the body, 
        for statement in body:        
               
             # translate assignment statement 
            if (len(statement) >= 3 and statement[1] in assignment):
                self.assignment(statement)
                
            # translates the function call. 
            elif ('(' in statement[0] and 'ret' not in statement[0]):
                self.funcCall(statement, 0)    

            # simply creates the goto and label code
            elif ('goto' in statement):
                self.goto(statement)

            # not sure about this part -.- 
            elif ('if' in statement):
                self.conditional(statement)
            
            elif ('ret' in statement or 'ret' in statement[0]):
                self.returnStmt(statement, mainFlag)
                flag = 0
        
        if (flag):
            self.returnStmt(None, mainFlag)

    # initialize the stack, create initial space on the stack for local variables
    def stackInitial(self, body, paramCount):
        
        tempCode = []
        tempCode.append(["push", "%rbp"])
        tempCode.append(["mov", "%rsp", "%rbp"])
        paramSize = 16
        for statement in body:
            stackLocation = "-" + str(self.stackSize) + "(%rbp)"
            if(len(statement) == 1 and ":" not in statement[0] and (statement[0] not in self.symbolTable.keys())):
                dict = {statement[0] : stackLocation}
                self.symbolTable.update(dict)

                dict = {"-" + statement[0] : stackLocation}
                self.symbolTable.update(dict)
                self.setReg.insertMemory("-" + statement[0], stackLocation)

                self.stackSize += 8
                self.setReg.insertMemory(statement[0], stackLocation)

            elif(len(statement) >= 3 and statement[1] == '=' and (statement[0] not in self.symbolTable.keys()) and ":" not in statement[0]):
                dict = {statement[0] : stackLocation}
                self.symbolTable.update(dict)

                dict = {"-" + statement[0] : stackLocation}
                self.symbolTable.update(dict)
                self.setReg.insertMemory("-" + statement[0], stackLocation)

                self.stackSize += 8
                self.setReg.insertMemory(statement[0], stackLocation)

        if (len(paramCount) != 0):
            for param in paramCount:
                stackLocation = "+" + str(paramSize) + "(%rbp)"
                dict = {param : stackLocation}
                self.symbolTable.update(dict)
                dict = {"-" + param : stackLocation}
                self.symbolTable.update(dict)
                self.setReg.insertMemory("-" + param, stackLocation)
                paramSize += 8
                self.setReg.insertMemory(param, stackLocation)


        tempCode.append(["sub", "$" + str(self.stackSize), "%rsp"])
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
            self.ass.append(["mov ", RHS, self.getMemLocation(LHS)])
        # assignment like a = add3(i, j)
        elif ("(" in RHS):
            RHS_list = RHS.split(" ")
            self.funcCall(RHS_list, 1)
            self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
            instructions = self.setReg.afterFunctionCall()
            self.ass.append([instructions.split("\n")[0]])
            self.ass.append([instructions.split("\n")[1]])
            self.ass.append([instructions.split("\n")[2]])
        # assignment like a = b will be tranlate to:
        # mov b_location %eax
        # mov %eax a_location
        # mov $0 %eax 
        else:
            #TODO self.setReg.movFromMem2Reg(str(RHS))
            #TODO The following 3 lines of code will be replaced with Yash's algorithm
            self.ass.append(["mov", self.getMemLocation(RHS), "%rax"])
            self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
        return
    
    def simpleArithmetic(self, statement):
        ops = statement[3]
        if (ops == '+' or ops == '-' or ops == '|' or ops == '&' or ops == '^'):
            self.plusAndMinusAndLogic(statement[0], statement[2], statement[4], ops, statement)
        elif (ops == '*'):
            self.times(statement[0], statement[2], statement[4], statement)
        elif (ops == '%' or ops == '/'):
            self.divideAndModulo(statement[0], statement[2], statement[4], ops, statement)
        elif (ops == '<<' or ops == '>>'):
            self.shift(statement[0], statement[2], statement[4], ops, statement)
        else:
            print('unknow ops\n')
            exit()


    def plusAndMinusAndLogic(self, LHS, RHS1, RHS2, ops, statement):

        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)
        
        # RHS1 = constant &&  RHS2 = constant
        if (constFlag1 and constFlag2):
            if (ops == '+'):
                result = RHS1 + RHS2
            elif (ops == '-'):
                result = RHS1 - RHS2
            elif (ops == '|'):
                result = RHS1 | RHS2
            elif (ops == '&'):
                result = RHS1 & RHS2
            elif (ops == '^'):
                result = RHS1 ^ RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])

        # RHS1 = constant &&  RHS2 = var/function call
        elif (constFlag1 and not constFlag2):
            
            # mov <RHS2> <reg1>
            
            # instruction = self.setReg.movFromMem2Reg(RHS2)
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS2)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # add <const>,<reg1> or sub 
            if (ops == '+'):
                self.ass.append(["add", "$"+str(RHS1) , reges])
            elif (ops == '-'):
                self.ass.append(["sub", "$"+str(RHS1) , reges])
            elif (ops == '|'):
                self.ass.append(["or", "$"+str(RHS1) , reges])
            elif (ops == '&'):
                self.ass.append(["and", "$"+str(RHS1) , reges])
            elif (ops == '^'):
                self.ass.append(["xor", "$"+str(RHS1) , reges])
            # mov <reg1>, <LHS>
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        # RHS1 = var/funcCall && RHS2 = constant
        elif (not constFlag1 and constFlag2):
            # mov <RHS1> <reg1>

            instruction = self.setReg.movFromMem2Reg_2(statement, RHS1)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])

            # add <const>,<reg1>
            if (ops == '+'):
                self.ass.append(["add", "$"+str(RHS2) , reges])
            elif (ops == '-'):
                self.ass.append(["sub", "$"+str(RHS2) , reges])
            elif (ops == '|'):
                self.ass.append(["or", "$"+str(RHS2) , reges])
            elif (ops == '&'):
                self.ass.append(["and", "$"+str(RHS2) , reges])
            elif (ops == '^'):
                self.ass.append(["xor", "$"+str(RHS2) , reges])
             # mov <reg1>, <LHS>
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        # RHS1 = var && RHS2 = var 
        elif (not constFlag1 and not constFlag2):

            # mov <RHS1> <reg1>
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS1)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # add <RHS2>,<reg1>`
            if (ops == '+'):
                self.ass.append(["add", self.getMemLocation(RHS2) , reges])
            elif (ops == '-'):
                self.ass.append(["sub", self.getMemLocation(RHS2) , reges])
            elif (ops == '|'):
                self.ass.append(["or", self.getMemLocation(RHS2) , reges])
            elif (ops == '&'):
                self.ass.append(["and", self.getMemLocation(RHS2) , reges])
            elif (ops == '^'):
                self.ass.append(["xor", self.getMemLocation(RHS2) , reges])

            # mov <reg1>, <LHS>
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])


    def times(self, LHS, RHS1, RHS2, statement):
        
        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)

        if (constFlag1 and constFlag2):
            result = RHS1 * RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])

        # this is the case where a constant times a varaible
        elif (constFlag1 and not constFlag2):
           
            # move RHS1 regs0
            # (flag, availableReg) = self.ig.get_availableReg(str(RHS1))
            availableReg = self.ig.getVertexRegisters(statement, str(RHS1))
            if (availableReg == None):
                print("error occurred. Variable not found in interference graph")
                sys.exit(1)
            self.ass.append(["mov", "$"+str(RHS1) , availableReg])

            # mov RHS2 regs
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS2)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # imul regs0 regs
            self.ass.append(["imul", availableReg , reges])
            # mov reg0 LHS 
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

        elif (not constFlag1 and constFlag2):
            
            # move RHS2 mem
            # location = self.addToMem(RHS2)
            # self.ass.append(["mov", "$"+str(RHS2) , location])
            # (flag, availableReg) = self.ig.get_availableReg(str(RHS2))
            availableReg = self.ig.getVertexRegisters(statement, str(RHS2))

            if (availableReg == None):
                print("error occurred. Variable not found in interference graph")
                sys.exit(1)
            self.ass.append(["mov", "$"+str(RHS1) , availableReg])

            # mov RHS1 reg1
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS1)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # imul RHS1 reg1
            self.ass.append(["imul", availableReg , reges])
            # mov reg1 LHS 
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])


        elif (not constFlag1 and not constFlag2):
            # mov RHS1 reg1 
            
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS1)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # imul RHS2 reg1
            self.ass.append(["imul", self.getMemLocation(RHS2) , reges])
            # mov reg1 LHS
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])
        

    def divideAndModulo(self, LHS, RHS1, RHS2, ops, statement):
        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)

        if (constFlag1 and constFlag2):
            if (ops == '/'):
                result = RHS1 / RHS2
                result = int(result)
            elif (ops == '%'):
                result = RHS1 % RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])
        
        # 500/b
        elif (constFlag1 and not constFlag2):
    
            # mov RSH1 %eax
            self.ass.append(["mov", "$"+str(RHS1) , "%rax"])
            # get most significant 32bits of reg1 store it in mem1
            self.ass.append(["idiv", self.getMemLocation(RHS2)])
            if(ops == '/'):
                # quotient in %eax
                self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
            else:
                # remainder in %edx 
                self.ass.append(["mov", "%rdx", self.getMemLocation(LHS)])
            

        # b/500
        elif (not constFlag1 and constFlag2):

            # mov b rdx and eax 
            self.ass.append(["mov", self.getMemLocation(RHS1) , "%rax"])
            self.ass.append(["mov", "%rax" , "%rdx"])
            self.ass.append(["shr", "$32" , "%rdx"])
            self.ass.append(["shl", "$32" , "%rax"])
            # mov 500 ebx 
            self.ass.append(["mov", "$"+str(RHS1) , "%rbx"])
            # idiv ebx 
            self.ass.append(["idiv", "%rbx"])
            # Place the quotient in eax and the remainder in edx.
            if(ops == '/'):
                # quotient in %eax
                self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
            else:
                # remainder in %edx 
                self.ass.append(["mov", "%rdx", self.getMemLocation(LHS)])
            
        # b/a
        elif (not constFlag1 and not constFlag2):
            
            # mov b rdx and eax 
            self.ass.append(["mov", self.getMemLocation(RHS1) , "%rax"])
            self.ass.append(["mov", "%rax" , "%rdx"])
            self.ass.append(["shr", "$32" , "%rdx"])
            self.ass.append(["shl", "$32" , "%rax"])
            # mov a ebx 
            self.ass.append(["mov", self.getMemLocation(RHS2) , "%rbx"])
            # idiv ebx 
            self.ass.append(["idiv", "%rbx"])
            # Place the quotient in eax and the remainder in edx.
            if(ops == '/'):
                # quotient in %eax
                self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
            else:
                # remainder in %edx 
                self.ass.append(["mov", "%rdx", self.getMemLocation(LHS)])

    def shift(self, LHS, RHS1, RHS2, ops, statement):
        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)
     

        if (constFlag1 and constFlag2):
            if(ops == "<<"):
                result = RHS1 << RHS2
            elif(ops == ">>"):
                result = RHS1 >> RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])
        # a = 10 << b
        elif (constFlag1 and not constFlag2):
            
            # mov 10 reg 
            # (flag, availableReg) = self.ig.get_availableReg(str(RHS1))
            availableReg = self.ig.getVertexRegisters(statement, str(RHS1))

            if (availableReg == None):
                print("error occurred. Variable not found in interference graph")
                sys.exit(1)
            self.ass.append(["mov", "$"+str(RHS1) , availableReg])
            # mov b rcx 
            self.ass.append(["mov", self.getMemLocation(RHS2) , "%rcx"])
            # shl cl reg 
            if (ops == "<<"):
                self.ass.append(["shl", "%cl" , availableReg])
            elif (ops == ">>"):
                self.ass.append(["shr", "%cl" , availableReg])
            # mov reg LHS
            self.ass.append(["mov", availableReg , self.getMemLocation(LHS)])
        # a = b << 10
        elif (not constFlag1 and constFlag2):

            # mov b reg 
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS1)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # shl 10 reg
            if (ops == "<<"):
                self.ass.append(["shl", "$" + str(RHS2), reges])
            elif (ops == ">>"):
                self.ass.append(["shr", "$" + str(RHS2), reges])

            self.ass.append(["mov", reges , self.getMemLocation(LHS)])
            
        # a = b << a
        elif (not constFlag1 and not constFlag2):
            
             # mov b reg 
            instruction = self.setReg.movFromMem2Reg_2(statement, RHS1)
            instruction1, instruction2, reges = self.splitMovFromMem2RegReturns(instruction)
            if(instruction2 != None):
                self.ass.append([instruction1])
                self.ass.append([instruction2])
            else: 
                self.ass.append([instruction1])
            # mov a rcx 
            self.ass.append(["mov", self.getMemLocation(RHS2) , "%rcx"])
            # shl cl reg 
            if (ops == "<<"):
                self.ass.append(["shl", "%cl" , reges])
            elif (ops == ">>"):
                self.ass.append(["shr", "%cl" , reges])
            # mov reg LHS
            self.ass.append(["mov", reges , self.getMemLocation(LHS)])

   
    def addToMem(self, var):
        stackLocation = "-" + str(self.stackSize) + "(%ebp)"
        dict = {var : stackLocation}
        self.stackSize += 8
        self.symbolTable.update(dict)
        self.setReg.insertMemory(str(var), stackLocation)
        return stackLocation

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

    def splitMovFromMem2RegReturns(self, instruciton):
        list = instruciton.split('\n')
        
        for item in list:
            if (item == ''):
                list.remove(item)
        if (len(list) == 2):
            reges = list[1].split(" ")[2]
            return list[0], list[1], reges
        else:
            reges = list[0].split(" ")[2]
            return list[0], None, reges


    def returnStmt(self, statement, flag):
        floatPatten = re.compile(r"[0-9]+\.[0-9]+")
        intPatten = re.compile(r"^[-+]?\d+$")
        
        if (statement != None):
            if (len(statement) <= 2):
                args = statement[1]
                if (intPatten.match(args) or floatPatten.match(args)):
                    location = args
                else:
                    location = self.getMemLocation(args)
                self.ass.append(["mov", location ,"%rax"])
            
            # return 1+2+3 or return function call
            else:
                if ("(" in statement[0]):
                    statement[0] = statement[0].replace('ret', "").strip()
                    self.funcCall(statement, 1)
                    instructions = self.setReg.afterFunctionCall()
                    self.ass.append([instructions.split("\n")[0]])
                    self.ass.append([instructions.split("\n")[1]])
        else:
            self.ass.append(["mov", "$0", "%rax"])

        if (not flag):
            instructions =self.setReg.calleeEnd()
            self.ass.append([instructions.split("\n")[0]])
            self.ass.append([instructions.split("\n")[1]])
            self.ass.append([instructions.split("\n")[2]])

        # Deallocate local variables
        self.ass.append(["mov", "%rbp" ,"%rsp"])
        
        # Restore the caller's base pointer value
        self.ass.append(["pop", "%rbp"])
        self.ass.append(["ret"])

    def goto(self, statement):
        pass

    def funcCall(self, statement, flag):
       
        # stores parameter inverse order 
        parameterList = []
        funcName = statement[0].replace('(', '').strip()
        # the caller saved registers : EAX, ECX, EDX
        instructions = self.setReg.callerSavedReg()
        self.ass.append([instructions.split("\n")[0]])
        self.ass.append([instructions.split("\n")[1]])
        self.ass.append([instructions.split("\n")[2]])
       
        # Push funcCall parameters to stack in inverse order
        
        parameterList = self.pushParameters(statement, funcName)

        # invoke the call instruction, return value stored in EAX 
       
        self.ass.append(["call", "_" + funcName])

        # after the return, pop parameters from stack
        self.popParameters(parameterList)

        # pop EAX, ECX, EDX
        if(not flag):
            instructions = self.setReg.afterFunctionCall()
            self.ass.append([instructions.split("\n")[0]])
            self.ass.append([instructions.split("\n")[1]])
            self.ass.append([instructions.split("\n")[2]])

    def pushParameters(self, statement, funcName):
        parameterList = []
        for item in statement:
            if ("(" not in item and ")" not in item and "," not in item and item != funcName):
                parameterList.append(item)
        temp = parameterList
        
        for item in parameterList[::-1]:
            self.ass.append(["push", self.getMemLocation(item)])
        return temp
    
    def popParameters(self, list):
        for item in list:
            self.ass.append(["pop", self.getMemLocation(item)])

    def funCallinExpr(self, RHS):
        RHS_list = RHS.split(" ")
        self.funcCall(RHS_list, 1)
        self.ass.append(["mov", "%rax" , self.getMemLocation(RHS)])
        instructions = self.setReg.afterFunctionCall()
        self.ass.append([instructions.split("\n")[0]])
        self.ass.append([instructions.split("\n")[1]])
        self.ass.append([instructions.split("\n")[2]])


    def printAssembly(self):
        str1 = " "
        indentFlag = 0
        for list in self.ass:
            if(len(list) == 1 and list[0][0] == '_'):
                print(list[0])
            else:
                # print(list)
                print('\t', str1.join(list))


    