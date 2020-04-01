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
        self.constantFolding()
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
        
    def constantFolding(self):
        funcCount = 0
        for func in self.functionBlock:
            funcEnd = func[1]
            leaderList = self.leaders[funcCount]
            
            # loop through all the basic blocks
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
                self.fold(basicBlockStart, basicBlockEnd)
                i += 1
                # print(basicBlockStart, basicBlockEnd)
            funcCount += 1

    def fold(self, startline, endline):
        basicBlock = self.IRS[startline:endline+1]
        for line in basicBlock:
            if (len(line) == 3 and line[1] == '=' and line[0] not in self.varValue.keys()):
                dict = {line[0] : line[2]}
                self.varValue.update(dict)
            elif (len(line) == 1 and ':' not in str(line[0]) and line[0] not in self.varValue.keys()):
                dict = {line[0] : None}
                self.varValue.update(dict)
        
        
        print(self.varValue)
        
    def propagation(self, startline, endline):
        pass

        # print(basicBlock)



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

    def printIR(self):
        pass
