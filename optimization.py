import re
from ply_scanner import arithmetic

class optimization:
    def __init__(self, IR):
        self.IRS = IR
        self.optimizedIR = [] 
        self.functionBlock = []
        self.leaders = []
        self.varValue = {}
    
    def run(self):
        self.findFunctionBlocks()
        self.findLeaders()
        self.removeDupLeader()
        self.invoke()
        self.removeLines()
        return self.IRS
    
    def findFunctionBlocks(self):
        lineNumber = 1
        funcStart = 0
        funcEnd = 0
        for line in self.IRS:
            if ('{' in line):
                funcStart =  lineNumber + 1
            elif ('}' in line):
                funcEnd = lineNumber - 1
                funcBlock = [funcStart, funcEnd]
                self.functionBlock.append(funcBlock)
                funcStart = 0
                funcEnd = 0
            lineNumber += 1
       
    def findLeaders(self):
        lineNumber = 1 
        gotoTraget = []
        for funcBlcoks in self.functionBlock:
            funcStart = funcBlcoks[0]
            funcEnd = funcBlcoks[1]
            leader = []
            lineNumber = funcStart - 1
            leader.append(lineNumber)
            while (lineNumber < funcEnd):
                line = self.IRS[lineNumber]
                if ('goto' in line):
                    gotoTraget.append(line[1])
                    leader.append(lineNumber + 1)
                lineNumber += 1
            lineNumber = funcStart - 1
            while (lineNumber < funcEnd):
                for target in gotoTraget:
                    if (target in self.IRS[lineNumber] and len(self.IRS[lineNumber]) == 1):
                        leader.append(lineNumber)
                lineNumber += 1
            self.leaders.append(leader)
        # print(self.leaders)
    
    def invoke(self):
        funcCount = 0

        for func in self.functionBlock:
            flag1 = 1
            flag2 = 1
            funcEnd = func[1]
            leaderList = self.leaders[funcCount]
            i = 0
            while (i < len(leaderList)):
                if (len(leaderList) == 1):
                    basicBlockStart = leaderList[0]
                    basicBlockEnd = funcEnd - 1
                else : 
                    if (i == len(leaderList) - 1):
                        basicBlockStart = leaderList[i] 
                        basicBlockEnd = funcEnd - 1
                    else:  
                        basicBlockStart = leaderList[i] 
                        basicBlockEnd = leaderList[i + 1] - 1
                # while (flag1 or flag2):
                while (flag1 or flag2):
                    flag1 = self.fold(basicBlockStart, basicBlockEnd)
                    flag2 = self.propagation(basicBlockStart, basicBlockEnd)
                i += 1
            # print(self.varValue)
            self.varValue = {}
            funcCount += 1
       


    def fold(self, startline, endline):
        basicBlock = self.IRS[startline:endline+1]
        lineNum = startline
        # use flag to identity if any changes happend 
        flag = 0
        for line in basicBlock:
            if (len(line) == 3 and line[1] == '=' and line[0] not in self.varValue.keys()):
                floatPatten = re.compile(r"[0-9]+\.[0-9]+")
                intPatten = re.compile(r"^[-+]?\d+$")
                if (intPatten.match(str(line[2]))):
                    dict = {line[0] : int(line[2])}
                    
                elif (floatPatten.match(str(line[2]))):
                    dict = {line[0] : float(line[2])}
                else:
                    dict = {line[0] : line[2]}
                self.varValue.update(dict)
            
            elif (len(line) == 3 and line[1] == '=' and line[0] in self.varValue.keys()):
                if (line[2] in self.varValue and (type(self.varValue[line[2]]) == int or type(self.varValue[line[2]]) == float)):
                        self.varValue[line[0]] = self.varValue[line[2]]
                        self.IRS[lineNum] = [line[0], line[1], self.varValue[line[2]]]
                        flag = 1

            elif (len(line) == 1 and ':' not in str(line[0]) and line[0] not in self.varValue.keys()):
                dict = {line[0] : None}
                self.varValue.update(dict)

            elif (len(line) > 3 and line[1] == '='):
                result = self.compute(line)
                if (result != 'N/A'):
                    flag = 1
                    self.IRS[lineNum] = [line[0], line[1], result]
                    if (line[0] not in self.varValue.keys()):
                        dict = {line[0] : result}
                        self.varValue.update(dict)
                    else:
                        self.varValue[line[0]] = result
            lineNum += 1
        return flag
        # print(self.varValue)
        
    def propagation(self, startline, endline):
        basicBlock = self.IRS[startline:endline+1]
        lineNum = startline
        flag = 0
        for line in basicBlock:
            index = 1
            for opand in line[1:]:
                if (len(line) > 3 and line[1] == '=' and opand in self.varValue and (type(self.varValue[opand]) == int or type(self.varValue[opand]) == float)):
                    self.IRS[lineNum][index] = self.varValue[opand]
                    flag = 1
                    if (line[0] in self.varValue.keys()):
                        del self.varValue[line[0]]
                elif ('(' in opand and ('int' in opand or 'float' in opand)):
                    if ('int' in opand):
                        opand = str(opand).replace('(int)', '').strip()
                        if (opand in self.varValue.keys()):
                            value = int(self.varValue[opand])
                            self.IRS[lineNum][index] = str(value)
                            flag = 1
                    elif ('float' in opand):
                        opand = str(opand).replace('(float)', '').strip()
                        if (opand in self.varValue.keys()):
                            value = float(self.varValue[opand])
                            self.IRS[lineNum][index] = str(value)
                            flag = 1
                index += 1
            lineNum += 1
        return flag
        # print(self.varValue)
        # print(self.IRS)
        # pass

    def compute(self, line):
        floatPatten = re.compile(r"[0-9]+\.[0-9]+")
        intPatten = re.compile(r"\d+")
        expr = []
        # flag is use to determine if the expression can be computed (e,g expr oprands are all int/float)
        flag = 'N/A'
        # if variable exits in the RHS of expr, stop the computing process.
        varCount = 0
        for oprnd in line:
            oprnd = str(oprnd)
            if (floatPatten.match(oprnd)):
                expr.append(float(oprnd))
            elif (intPatten.match(oprnd)):
                expr.append(int(oprnd))
            elif (oprnd in arithmetic or oprnd == '='):
                expr.append(oprnd)
            else:
                if (not varCount):
                    varCount += 1
                    expr.append(oprnd)
                else:
                    return flag 
        result = self.simpleArithmetic(expr[2],expr[3],expr[4])
        return str(result)

    # remove var decls and assignments which the variable is not used 
    # in anywhere else inside the function
    def removeLines(self):
        for funcBlcoks in self.functionBlock:
            # keep track how many times the variable is referenced 
            varRefCount = {}
            varLocation = []
            funcStart = funcBlcoks[0] - 1
            funcEnd = funcBlcoks[1]
            lineNum = funcStart
            while(lineNum < funcEnd):
                line = self.IRS[lineNum]
                # Var decl without assigment 
                if(len(line) == 1 and ':' not in line[0]):
                    dict = {line[0] : 0}
                    varRefCount.update(dict)
                    varLocation.append(lineNum)
                elif(len(line) >= 3 and line[1] == '='):
                    if(line[0] in varRefCount.keys()):
                        varRefCount[line[0]] = 1
                    else:
                        dict = {line[0] : 0}
                        varRefCount.update(dict)
                        varLocation.append(lineNum)
                else:
                    for key in varRefCount.keys():
                        for opand in line:
                            if(key == opand):
                                varRefCount[key] = 1
                lineNum += 1

            locationIndex = 0
            for key in varRefCount.keys():
                if(varRefCount[key] == 0):
                    self.IRS[varLocation[locationIndex]] = ''        
                locationIndex += 1

            while('' in self.IRS): 
                self.IRS.remove('') 

    def removeDupLeader(self):
        res = []
        for leader in self.leaders:
            temp = []
            for i in leader:
                if i not in res:    
                    temp.append(i)
            temp.sort()
            res.append(temp)
        # print(res)

    def simpleArithmetic(self, opnd1, oprt, opnd2):
        result = 0 
        if (oprt == '+'):
            result = opnd1 + opnd2
        elif (oprt == '-'):
            result = opnd1 - opnd2
        elif (oprt == '*'):
            result = opnd1 * opnd2
        elif (oprt == '/'):
            result = opnd1 / opnd2
        elif (oprt == '%'):
            result = opnd1 % opnd2
        elif (oprt == '|'):
            result = opnd1 | opnd2
        elif (oprt == '&'):
            result = opnd1 & opnd2
        elif (oprt == '^'):
            result = opnd1 ^ opnd2
        elif (oprt == '<<'):
            result = opnd1 << opnd2
        elif (oprt == '>>'):
            result = opnd1 >> opnd2
        return result

    def printIR(self):
        str1 = " "
        indentFlag = 0
        for list in self.IRS:
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
