'''
Class that handles the translation from the 
linear 3-address intermediate representation 
to x86-64 assembly code.
'''
from ply_scanner import assignment, comparison
from ply_scanner import arithmetic
from ply_scanner import logical
import re

class assembly3:
    def __init__(self, ir, ig, setReg, ir_str):
        self.IR = ir
        self.ass = []
        self.ig = ig
        self.setReg = setReg
        self.symbolTable = {}
        self.stackSize = 8
        self.ir_str = ir_str
    
    # this function splits the input IR to different functions
    # each function's body is stored in a list and passed to
    # other function to translate 
    def run(self):
        lineNumber = 0
        funcScope = []
        funcScope2 = []
        flag = 0
        name = ""
        paramCount = 0
        self.ig.run(self.setReg)

        for line, stmt in zip(self.IR, self.ir_str.split('\n')):
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
                self.funcBody(funcScope, name, paramCount, funcScope2)
                funcScope = []
                funcScope2 = []
            elif (flag):
                funcScope.append(line)
                funcScope2.append(stmt)
            lineNumber += 1
        self.printAssembly()
    
    # funcName function appends the funcation name to 
    # the final assembly code list, the function name 
    # will start with '_' 
    def funcName(self, line):
        # creates function label, creates assembly code to handel args if exist. 
        self.ass.append(["_" + line[0]])
        paramCount = []
        for item in line:
            if ("(" not in item and ")" not in item and "," not in item and item != line[0]):
               paramCount.append(item)
        return "_" + line[0], paramCount

    # funcBody handles the code generation of
    # statements inside funciton body. we scan through
    # each line of the input IR, and determine which function
    # should be called to perform the conversion. 
    def funcBody(self, body, name, paramCount, funcScope2):

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
        for statement, statement2 in zip(body, funcScope2):        
               
             # translate assignment statement 
            if (len(statement) >= 3 and statement[1] in assignment):
                self.assignment(statement, statement2)
                
            # translates the function call. 
            elif ('(' in statement[0] and 'ret' not in statement[0]):
                self.funcCall(statement, 0)    

            # simply creates the goto and label code
            elif (re.match(r'goto', statement[0])):
                self.goto(statement, statement2)

            # handle if/else, else will be from loops
            elif ('if' in statement[0]):
                if ('else' in statement):
                    self.loop(statement, statement2)
                else:
                    self.conditional(statement, statement2)
            
            # Statement is a label
            elif (re.match(r'L[0-9]+:', statement[0])):
                self.label(statement, statement2)
            
            elif ('ret' in statement or 'ret' in statement[0]):
                self.returnStmt(statement, mainFlag)
                flag = 0
        
        if (flag):
            self.returnStmt(None, mainFlag)

    # initialize the stack pointers
    # create initial space on the stack for local variables
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

    # the function Takes variable name as input,
    # returns its corresponding mem location
    # return will be something like -4(%ebp)
    def getMemLocation(self, var):
        if(var not in self.symbolTable):
            print("var not on the stack")
        else:
            return self.symbolTable[var]
    
    # Takes a variable and returns the register where it is stored
    # If it exists
    def getRegister(self, var):
        for k, v in self.setReg.symboltable_reg.items():
            if (v == var):
                # Register located
                return k

        return None

    # Assignment funciton handles simple assignment like a = 1
    # and assignment with arithmetic, a = 1 + b
    def assignment(self, statement, statement2):
        if (len(statement) == 3 ):
            self.simpleAssign(statement[0], statement[2])
        elif (statement[3] in arithmetic):
            self.simpleArithmetic(statement, statement2)
        
    # SimpleAssign function converts assignment expressions 
    # which does not involve arithmetric operations 
    def simpleAssign(self, LHS, RHS):
        floatPatten = re.compile(r"[0-9]+\.[0-9]+")
        intPatten = re.compile(r"^[-+]?\d+$")
        # assignment like a = 2 will be translate to 'mov $2 a_location'
        if (intPatten.match(RHS) or floatPatten.match(RHS)):
            RHS = "$" + str(RHS)
            self.ass.append(["mov", RHS, self.getMemLocation(LHS)])
        # assignment like a = add3(i, j)
        elif ("(" in RHS):
            RHS_list = RHS.split(" ")
            self.funcCall(RHS_list, 1)
            self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
            instructions = self.setReg.afterFunctionCall()
            self.ass.append([instructions.split("\n")[0]])
            self.ass.append([instructions.split("\n")[1]])
            self.ass.append([instructions.split("\n")[2]])
        else:
            #TODO self.setReg.movFromMem2Reg(str(RHS))
            #TODO The following 3 lines of code will be replaced with Yash's algorithm
            self.ass.append(["mov", self.getMemLocation(RHS), "%rax"])
            self.ass.append(["mov", "%rax", self.getMemLocation(LHS)])
        return
    
    # SimpleArithmetric converts arithmetric expression to assembly code
    def simpleArithmetic(self, statement, statement2):
        ops = statement[3]
        if (ops == '+' or ops == '-' or ops == '|' or ops == '&' or ops == '^'):
            self.plusAndMinusAndLogic(statement[0], statement[2], statement[4], ops, statement2)
        elif (ops == '*'):
            self.times(statement[0], statement[2], statement[4], statement2)
        elif (ops == '%' or ops == '/'):
            self.divideAndModulo(statement[0], statement[2], statement[4], ops)
        elif (ops == '<<' or ops == '>>'):
            self.shift(statement[0], statement[2], statement[4], ops, statement2)
        else:
            print('unknow ops\n')
            exit()

    # Converts plus, minus and logic operation. 
    # The expression will be divided into Left Hand
    # Right Hand Side 1 and Right Hand Side 2
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

    # The functions converts multiplication expression into assembly code 
    def times(self, LHS, RHS1, RHS2, statement):
        result = '0'
        constFlag1, constFlag2, RHS1, RHS2 = self.determineConstant(RHS1, RHS2)

        if (constFlag1 and constFlag2):
            result = RHS1 * RHS2
            self.ass.append(["mov", "$"+str(result) , self.getMemLocation(LHS)])

        # this is the case where a constant times a varaible
        elif (constFlag1 and not constFlag2):
           
            # move RHS1 regs0
            (flag, availableReg) = self.ig.getVertexRegisters(statement, str(RHS1))
            if (availableReg == None):
                print("error occurred. Variable not found in interference graph")
                sys.exit(1)
            self.ass.append(["mov", "$"+str(RHS1) , availableReg])

            # mov RHS2 regs
            instruction = self.setReg.movFromMem2Re_2(statement, RHS2)
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
            (flag, availableReg) = self.ig.getVertexRegisters(statementstr(RHS2))
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
        
    # The functions converts division operation into assembly code 
    def divideAndModulo(self, LHS, RHS1, RHS2, ops):
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

     # The functions converts shift operation into assembly code 
    def shift(self, LHS, RHS1, RHS2, ops,statement):
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
            (flag, availableReg) = self.ig.getVertexRegisters(statement,str(RHS1))
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

    # Helper function that create an addtional space on stack
    # input will be variable name 
    # returns the stack offset 
    def addToMem(self, var):
        stackLocation = "-" + str(self.stackSize) + "(%ebp)"
        dict = {var : stackLocation}
        self.stackSize += 8
        self.symbolTable.update(dict)
        self.setReg.insertMemory(str(var), stackLocation)
        return stackLocation

    # Helper function that determines if inputs are number or string
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

    # Small helper function that helps with spliting an instrunction
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

    # Converts return statement into assembly code
    # and also do some house keeping when the function returns 
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

    # Translate goto statment from IR to assembly
    def goto(self, statement, statement2):
        if (len(statement) == 2):
            label = statement[1]
        else:
            label = list(filter(None, re.split(r'goto |:', statement[0])))[0]

        self.ass.append(["jmp {}".format('_' + label)])

        return

    # Translate label from IR to Assembly
    def label(self, label, statement2):
        self.ass.append(['_' + label[0]])
        return

    # Check if operands are located in registers
    # Useful for checking if an operand needs to be moved to a reg
    # For cases when there is no mem-mem instr available
    def operandCheck(self, operands):
        regs = []
        for op in operands:
            if (op in self.setReg.symboltable_reg.values()):
                # Operand 1 is stored in a register
                regs.append(self.getRegister(op))
            else:
                # Operand 1 is not stored in a register  
                regs.append(None)

        return regs

    # Translate conditional statments from IR to Assembly
    def conditional(self, statement, statement2):
        needRegAlloc = True
        # Split statement into list of statements; split by 'if' and 'goto' (re.split(r'if|goto'))
        expr, jmp_label = list(filter(None, re.split(r'if | goto |:', statement[0])))
        operand1, operator, operand2 = expr.split(' ')
        
        # Check if at least one variable is in a register; if neither are, insert one into register
        operands = self.operandCheck([operand1, operand2])

        # Write cmp to ass with correct reg/mem or mem/reg or reg/con
        if (needRegAlloc):
            # Assign operand 1 to register
            tmp = self.setReg.movFromMem2Reg_2(statement2, operand1)
            self.ass.append([tmp])
            operand1_reg = self.getRegister(operand1)

            if (re.match(r'[0-9]*', operand2)):
                # cmp <reg>, <con>
                self.ass.append(["cmp {}, ${}".format(operand1_reg, operand2)])
            else:
                # cmp <reg>, <mem>
                self.ass.append(["cmp {}, {}".format(operand1_reg, self.getMemLocation(operand2))])
        else:
            if (operands[0] is not None):
                # Operand 1 is stored in a register
                self.ass.append(["cmp {}, {}".format(operands[0], self.getMemLocation(operand2))])
            else:
                self.ass.append(["cmp {}, {}".format(self.getMemLocation(operand1), operands[1])])

        # Determine which jump needs to be performed based on operator
        # Write correct jmp with correct label
        if (operator == '=='):
            self.ass.append(["je {}".format('_' + jmp_label)])
        elif (operator == '!='):
            self.ass.append(["jne {}".format('_' + jmp_label)])
        elif (operator == '<'):
            self.ass.append(["jl {}".format('_' + jmp_label)])
        elif (operator == '>'):
            self.ass.append(["jg {}".format('_' + jmp_label)])
        elif (operator == '<='):
            self.ass.append(["jle {}".format('_' + jmp_label)])
        elif (operator == '>='):
            self.ass.append(["jge {}".format('_' + jmp_label)])

        return

    # Converts loops from IR to assembly
    def loop(self, statement, statement2):
        needRegAlloc = True
        # split up ir. 
        # NOTE: comparison expr should be the second element in statement
        if_label = statement[3]
        jmp_label = if_label
        else_label = '_' + statement[-1]

        # find comparison operator
        for operator in comparison:
            if operator in statement[1]:
                compare = operator
                break;
        operand1, operand2 = statement[1].split(compare)
        operator = compare
        
        # Check if at least one variable is in a register; if neither are, insert one into register
        operands = self.operandCheck([operand1, operand2])

        # Write cmp to ass with correct reg/mem or mem/reg or reg/con
        if (needRegAlloc):
            # Assign operand 1 to register
            self.ass.append([self.setReg.movFromMem2Reg_2(statement2, operand1)])
            
            operand1_reg = self.getRegister(operand1)

            if (re.match(r'[0-9]*', operand2)):
                # cmp <reg>, <con>
                self.ass.append(["cmp {}, ${}".format(operand1_reg, operand2)])
            else:
                # cmp <reg>, <mem>
                self.ass.append(["cmp {}, {}".format(operand1_reg, self.getMemLocation(operand2))])
        else:
            if (operands[0] is not None):
                # Operand 1 is stored in a register
                self.ass.append(["cmp {}, {}".format(operands[0], self.getMemLocation(operand2))])
            else:
                self.ass.append(["cmp {}, {}".format(self.getMemLocation(operand1), operands[1])])

        # Determine which jump needs to be performed based on operator
        # Write correct jmp with correct label
        if (operator == '=='):
            self.ass.append(["je {}".format('_' + jmp_label)])
        elif (operator == '!='):
            self.ass.append(["jne {}".format('_' + jmp_label)])
        elif (operator == '<'):
            self.ass.append(["jl {}".format('_' + jmp_label)])
        elif (operator == '>'):
            self.ass.append(["jg {}".format('_' + jmp_label)])
        elif (operator == '<='):
            self.ass.append(["jle {}".format('_' + jmp_label)])
        elif (operator == '>='):
            self.ass.append(["jge {}".format('_' + jmp_label)])

        self.ass.append(['jmp', else_label])

        return

    # converts function call to aseembly
    # this will push registers that are caller saved
    # push parameters and invoke the call instruction 
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

    # Helper function used in funCall, used to push the function call
    # parameters to the stack
    def pushParameters(self, statement, funcName):
        parameterList = []
        for item in statement:
            if ("(" not in item and ")" not in item and "," not in item and item != funcName):
                parameterList.append(item)
        temp = parameterList
        
        for item in parameterList[::-1]:
            self.ass.append(["push", self.getMemLocation(item)])
        return temp
    
    # Helper function that generate pop instruction 
    def popParameters(self, list):
        for item in list:
            self.ass.append(["pop", self.getMemLocation(item)])

    # Helper function that append some instructions to the code
    def funCallinExpr(self, RHS):
        RHS_list = RHS.split(" ")
        self.funcCall(RHS_list, 1)
        self.ass.append(["mov", "%rax" , self.getMemLocation(RHS)])
        instructions = self.setReg.afterFunctionCall()
        self.ass.append([instructions.split("\n")[0]])
        self.ass.append([instructions.split("\n")[1]])
        self.ass.append([instructions.split("\n")[2]])

    # printing function 
    def printAssembly(self):
        str1 = " "
        indentFlag = 0
        for list in self.ass:
            if(len(list) == 1 and list[0][0] == '_'):
                print(list[0])
            else:
                print('\t', str1.join(list))
