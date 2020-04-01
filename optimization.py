class optimization:
    def __init__(self, IR):
        self.IRS = IR
        self.optimizedIR = [] 
        self.functionBlock = []
        self.leaders = []
    
    def run(self):
        self.findFunctionBlocks()
        self.findLeaders()
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
            leader.append(funcStart)
            while (lineNumber < funcEnd):
                line = self.IRS[lineNumber]
                if ('goto' in line):
                    gotoTraget.append(line[1])
                    leader.append(lineNumber + 2)
                lineNumber += 1
            
            lineNumber = funcStart - 1
            while (lineNumber < funcEnd):
                for target in gotoTraget:
                    if (target in self.IRS[lineNumber] and len(self.IRS[lineNumber]) == 1):
                        leader.append(lineNumber + 1)
                lineNumber += 1
            
            leader.append(funcEnd)
            self.leaders.append(leader)

        print(self.leaders)
            




    def printIR(self):
        pass
