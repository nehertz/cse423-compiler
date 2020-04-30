import re
import sys

class SymbolTableRegisters:
    def __init__(self, ir, ig):
        self.symboltable_reg = {}
        self.symboltable_mem = {}
        # variable names as keys and their memory location as addresses. 
        self.initiate_st_reg()
        self.number = re.compile(r'\d+')
        self.ig = ig
    
    def movFromReg2Mem(self, reg):
        # updates the symbol table
        # returns the assembly code
        tmpVar = self.symboltable_reg[reg]
        if (self.number.match(tmpVar)):
            self.symboltable_reg[reg] = ''
        else:
            memAddr = self.symboltable_mem[tmpVar]
            assCode = 'mov ' + str(self.symboltable_reg[reg]) + ' ' + str(memAddr) + '\n'
            self.symboltable_reg[reg] = ''
        return assCode
    # 4(%rsp)
    def insertMemory(self, var, memory_location):
        self.symboltable_mem[var] = memory_location
        return

    def movFromMem2Reg(self, var):
        # updates the symbol table
        # returns the assembly code
        # get designed available register for that variable 
        (flag, availableReg) = self.ig.get_availableReg(var)
        if (availableReg == None):
            print("error occurred. Variable not found in interference graph")
            sys.exit(1)
        if (flag == False):
            # it's a memory location - remove unnecessary/temporary registers
            pass
        assCode = ''
        if (self.symboltable_reg[availableReg] != ''):
            name_var = self.symboltable_reg[availableReg]
            assCode += 'mov ' + str(availableReg) + ' ' + str(self.symboltable_mem[name_var])
            assCode += '\n'
            self.symboltable_reg[availableReg] = ''

        assCode += 'mov ' + str(self.symboltable_mem[var]) + ' ' + str(availableReg)
        assCode += '\n'
        self.symboltable_reg[availableReg] = var
        return assCode
    
    def initiate_st_reg(self):
        self.symboltable_reg['%rax'] = ''
        self.symboltable_reg['%rcx'] = ''
        self.symboltable_reg['%rdx'] = ''
        self.symboltable_reg['%rbx'] = ''
        self.symboltable_reg['%rsi'] = ''
        self.symboltable_reg['%rdi'] = ''
        self.symboltable_reg['%rsp'] = ''
        self.symboltable_reg['%rbp'] = ''
        self.symboltable_reg['%r8'] = ''
        self.symboltable_reg['%r9'] = ''
        self.symboltable_reg['%r10'] = ''
        self.symboltable_reg['%r11'] = ''
        self.symboltable_reg['%r12'] = ''
        self.symboltable_reg['%r13'] = ''
        self.symboltable_reg['%r14'] = ''
        self.symboltable_reg['%r15'] = ''
        

    def callerSavedReg(self):
        '''
        1. Caller-saved Register: %eax, %ecx, %edx. 
        caller should push these values on the stack. 
        2. Pass the parameters by pushing them on stack and also last parameter first order (inverted).
        3. push the return address on top of the stack. 
        '''
            


        return assCode
    def check_reg_status(self, reg):
        if (self.symboltable_reg[reg] == ''):
            return True
        return False