class optimization:
    def __init__(self, IR):
        self.IRS = IR
        self.optimizedIR = [] 
        self.leaders = []
    
    def run(self):
        self.findLeaders()

        return self.IRS
    
    def findLeaders(self):
        lineNumber = 1 
        gotoTraget = []
        for line in self.IRS:
            # the first 3-address code of a function is leader 
            if ('{' in line):
                self.leaders.append(lineNumber + 1)
            # instruction that immediately follows jump is leader 
            elif ('goto' in line):
                gotoTraget.append(line[1]) 
                self.leaders.append(lineNumber + 1)
            lineNumber += 1
            # print(line)
        # instruction that is the traget of jump is leader
        lineNumber = 1 
        for line in self.IRS:
            for target in gotoTraget:
                if (target in line):
                    self.leaders.append(lineNumber + 1)
            lineNumber += 1
        print(self.leaders)

    def printIR(self):
        pass
