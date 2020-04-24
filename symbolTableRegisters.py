

class SymbolTableRegisters:
    def __init__(self):
        self.symboltable_reg = {}
        self.symboltable_mem = {}
    def insert(self):
        return

    def movFromReg2Mem(self, var):
        # updates the symbol table
        # returns the assembly code
        memAddr = self.symboltable_mem[var]
        assCode = 'mov ' + str(self.symboltable_reg[var]) + ' ' + str(memAddr)
        self.symboltable_reg[var] = ''
        return assCode

    def movFromMem2Reg(self, var):
        # updates the symbol table
        # returns the assembly code
        regAddr = self.symboltable_reg[var]
        # get available register
        return
    def initiate_st_mem(self):
        self.symboltable_mem['%rax'] = ''
        self.symboltable_mem['%rcx'] = ''
        self.symboltable_mem['%rdx'] = ''
        self.symboltable_mem['%rbx'] = ''
        self.symboltable_mem['%rsi'] = ''
        self.symboltable_mem['%rdi'] = ''
        self.symboltable_mem['%rsp'] = ''
        self.symboltable_mem['%rbp'] = ''
        self.symboltable_mem['%r8'] = ''
        self.symboltable_mem['%r9'] = ''
        self.symboltable_mem['%r10'] = ''
        self.symboltable_mem['%r11'] = ''
        self.symboltable_mem['%r12'] = ''
        self.symboltable_mem['%r13'] = ''
        self.symboltable_mem['%r14'] = ''
        self.symboltable_mem['%r15'] = ''
        
    