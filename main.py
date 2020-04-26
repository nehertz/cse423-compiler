import sys
import getopt
import re
from os import path
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_scanner import tokenizer
from ply_parser import parser
from ply_parser import st
from typeChecking import TypeChecking
from IR import IR
from optimization import optimization
from assembly import assembly
from symbolTableRegisters import SymbolTableRegisters
from interferenceGraph import *
# Print usage instructions for the compiler
# parameters: None
def printHelp():
    print("usage: main.py [-t] [-p] filename")
    print("-t   :print the sequence of tokens and labels")
    print("-p   :print abstract syntax tree ")
    print("-s   :print symbol table ")
    print("-i   :print IR ")
    print("-o   :write IR into a file")
    print("-r   :read IR from a file")
    print("-m   :turn on optimization pass")
    print("-h   :print the usage information")
    print("Default   :print option -t")

# Print the tokens and labels output by the scanner
# parameters: lexer, lexer object generated by PLY 
def printTokens(lexer):
    for tok in lexer:
        print("Token['" + str(tok.value)+ "' , '" + tok.type + "']")

# Print the abstract syntax tree generated from the parser
# The function uses skbio module to parse/print the tree
# parameters: ast, ast string contains tree structure in newick format
def printAST(ast):
    f = StringIO(ast)
    tree = read(f, format="newick",into=TreeNode)
    f.close
    print(tree.ascii_art())


def writeIRtoFile(IR, outputFile):
    try:
        f = open(outputFile, 'w')
    except OSError:
        print("ERROR: Could not write to " + outputFile + ".")
    with f:
        str1 = " "
        indentFlag = 0
        for list in IR:
            if (str1.join(list) == '{'):
                indentFlag = 1
                f.write(str1.join(list) + '\n')
                continue
            elif (str1.join(list) == '}'):
                indentFlag = 0
                f.write(str1.join(list) + '\n')
                continue
            elif (indentFlag):
                f.write('\t' + str1.join(list) + '\n')
            else:
                f.write(str1.join(list) + '\n' )
        f.close()

if __name__ == "__main__":
    cmdArgument = sys.argv
    listArgs = cmdArgument[1:]
    flag = 0  # flag that tells us which options are enabled
    optimizationFlag = 0
    inputFile = ' '
    outputFile = ' '
    ir = ' '

    # Check that the user has supplied enough arguments
    if not len(listArgs):
        print("Please include a filename.")
        printHelp()
        sys.exit()

    unixOptions = "htpsiormag"
    gnuOptions = ["help", "tokenize", "parse-tree", "symbol-table", "IR", "write-to-file", "read-from-file", "optimization-pass", "assembly", "register-allocation-first"]

    try:
        arguments, values = getopt.getopt(listArgs, unixOptions, gnuOptions)
    except getopt.error as err:
        # Output error
        print(str(err))
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if (currentArgument in ("-t", "--tokenize")):
            flag = 1
        if (currentArgument in ("-p", "--parse-tree")):
            flag = 2
        if (currentArgument in ("-s", "--symbol-table")):
            flag = 3
        if (currentArgument in ("-i", "--IR")):
            flag = 4
        if (currentArgument in ("-o", '--write-to-file')):
            flag = 5
        if (currentArgument in ("-r", '--read-from-file')):
            flag = 6
        if (currentArgument in ("-m", '--optimization-pass')):
            optimizationFlag = 1
        if (currentArgument in ("-a", '--assembly')):
            flag = 7
        if (currentArgument in ("-g", "-register-allocation-first")):
            flag = 8
        if (currentArgument in ("-h", "--help")):
            printHelp()
            sys.exit()

    # Check that the user has supplied a valid input file (as last arg)
    if (flag == 5):
        inputFile = listArgs[1]
        outputFile = listArgs[-1]
    else:
        inputFile = listArgs[-1]

    if (not path.exists(inputFile)):
        # File does not exist
        print("File {} doesn't exist ".format(inputFile))
        printHelp()
        sys.exit()

    # Perform compilation of the input program
    try:
        f = open(inputFile, 'r')
    except OSError:
        print("ERROR: Could not open/read " + inputFile + ".")
    with f:
        # Read the IR from a file, skip the tokenizer and parser
        if (flag == 6):
            fileString = f.readlines()
            ir = IR(None)
        else :
            fileString = f.read()
            lexer = tokenizer(fileString)
            ast = parser(lexer.clone())
            tc = TypeChecking(ast)
            ast = tc.run()
            ir = IR(ast)
        f.close()        

    # Print tokens with labels
    if (flag == 1 or flag == 0):
        printTokens(lexer)

    # Print the AST
    elif (flag == 2):       
        printAST(ast)

    # Print the symbol table 
    elif (flag == 3):
        st.print()

    # Prints the optimized version of the IR when the optimization flag is on 
    elif (flag == 4 and optimizationFlag == 1):
        IR = ir.run()
        ir.printIR()
        optimizedIR = optimization(IR)
        optimizedIR.run()
        optimizedIR.printIR()

    # Prints the original version of the IR when the optimization flag is off
    elif (flag == 4 and optimizationFlag == 0):
        printAST(ast)
        IR = ir.run()
        ir.printIR()
    
    # Write the IR into an output file
    elif (flag == 5):
        IR = ir.run()
        writeIRtoFile(IR, outputFile)

    # Read the IR from an input file
    elif (flag == 6):
        ir.readIR(fileString)
        ir.printIR()
    
    # Print the assembly when the optimization flag is on
    elif (flag == 7 and optimizationFlag == 1):
        IR = ir.run()
        optimizedIR = optimization(IR)
        IR = optimizedIR.run()
        assembly = assembly(IR)
        assembly.run()

        
    # Print the assembly when the optimization flag is off      
    elif (flag == 7 and optimizationFlag == 0):
        IR = ir.run()
        assembly = assembly(IR)
        assembly.run()

    elif (flag == 8):
        ir_str = ir.run()
        ir_str = ir.getIR()
        print(ir_str)
        ig = InterferenceGraph(ir_str)
        StReg = SymbolTableRegisters(ir_str)
        ig.run()