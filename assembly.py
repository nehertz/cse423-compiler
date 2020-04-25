from ply_scanner import assignment
from assembly_assign import *

class assembly:
    def __init__(self, ir):
        self.IR = ir
        self.ass = []

    
    def run(self):
        lineNumber = 0
        funcScope = []
        flag = 0
        for line in self.IR:
            # translate function name and args to assembly 
            if ('(' in line and ')' in line and self.IR[lineNumber+1][0] == '{'):
                self.funcName(line)

            # translate function statement body to assembly 
            elif ('{' in line):
                flag = 1
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
        pass

    def funcBody(self, body):
        # preparation: scanns the body to know how much stack spaces needed 
        size = self.getVarSizes(body)

        # initialize the stack, create initial space on the stack for local variables
        self.stackInitial(size)

        # scanning through the body, 
        for statement in body:
            # translate assignment statement 
            if (len(statement) >= 3 and statement[1] in assignment):
                self.assignment(statement)
            
            # simply creates the goto and label code
            elif ('goto' in statement):
                self.goto(statement)

            # not sure about this part -.- 
            elif ('if' in statement):
                self.conditional(statement)

            # translates the function call. 
            elif ('(' in statement and ')' in statement):
                self.funcCall(statement)            

    def getVarSizes(self, body):
        # use token table to obtain the size that stack should reserve 
        pass

    def stackInitial(self, size):
        # creates the stack initialization code 
        pass     
    
    def assignment(self, statement):
        # Assignment should handles simple assignment like a = 1
        # and assignment with arithmetic, a = 1 + b
        # One special case: function call in arithmetic. 
        if (len(statement) == 3 ):
            simpleAssign(statement[0], statement[2], self.ass)

        elif (statement[3] == '+'):
            plus(statement[0], statement[2], statement[4])
        
        elif (statement[3] == '-'):
            minus(statement[0], statement[2], statement[4])

        #....keep going 

    def funcCall(self, statement):
        pass
    
    def printAssembly(self):
        str1 = " "
        indentFlag = 0
        for list in self.ass:
            if (str1.join(list) == '{'):
                indentFlag = 1
                print(str1.join(list))
                continue
            elif (str1.join(list) == '}'):
                indentFlag = 0
                print(str1.join(list))
                continue
            elif (indentFlag):
                print('\t', str1.join(list))
            else:
                print(str1.join(list))


    