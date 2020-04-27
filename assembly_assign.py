import re 
floatPatten = re.compile(r"[0-9]+\.[0-9]+")
intPatten = re.compile(r"^[-+]?\d+$")
#<src><dest>
#`mov <reg>,<reg>`
#`mov <reg>,<mem>`
#`mov <mem>,<reg>`
#`mov <const>,<reg>`
#`mov <const>,<mem>`

def simpleAssign(LHS, RHS, assembly):
    #Find location of LHS, is it in memory stack or register. 
    #location = findLocation(LHS)
    
    #RHS could be varible or constant. 
    if (intPatten.match(RHS) or floatPatten.match(RHS)):
        #need to find the location of LHS 
        RHS = "$" + str(RHS)
        assembly.append(["mov", RHS, LHS])
    else:
        #need to find the location of LHS and RHS
        assembly.append(["mov", RHS, LHS])
    return

def simpleArithmetic(statement, assembly):
    ops = statement[3]
    if (ops == '+'):
        plus(statement[0], statement[2], statement[4], assembly)
    elif (ops == '-'):
        minus(statement[0], statement[2], statement[4], assembly)
    elif (ops == '*'):
        times(statement[0], statement[2], statement[4], assembly)
    elif (ops == '/'):
        divide(statement[0], statement[2], statement[4], assembly)
    elif (ops == '%'):
        modulo(statement[0], statement[2], statement[4], assembly)
    else:
        print('unknow ops\n')
        exit()

def plus(LHS, RHS1, RHS2, assembly):
    pass

def minus(LHS, RHS1, RHS2, assembly):
    pass

def times(LHS, RHS1, RHS2, assembly):
    pass

def divide(LHS, RHS1, RHS2, assembly):
    pass

def modulo(LHS, RHS1, RHS2, assembly):
    pass



