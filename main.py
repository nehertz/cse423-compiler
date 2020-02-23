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
# Print the instruction of how to excute the program
# parameters: None
def printHelp():
    print("usage: main.py [-t] [-p] filename")
    print("-t   :print the sequence of tokens and labels")
    print("-p   :print abstract syntax tree ")
    print("-s   :print symbol table ")
    print("-h   :print the usage information")
    print("Default   :print option -t")

# Print the tokens with its labels.
# parameters: lexer, lexer object generated by PLY 
def printTokens(lexer):
    for tok in lexer:
        print("Token['" + str(tok.value)+ "' , '" + tok.type + "']")

# Print the abstract syntax tree
# The function uses skbio module to parser/print the tree
# parameters: ast, ast string contains tree structure in newick format

# def printAST(ast):
#     f = StringIO(ast)
#     tree = read(f, format="newick",into=TreeNode)
#     f.close
#     print(tree.ascii_art())

if __name__ == "__main__":

    cmdArgument = sys.argv
    listArgs = cmdArgument[1:]
    flag = 0  # flag that tells us which options are enabled

    # Check that the user has supplied enough arguments
    if not len(listArgs):
        print("Please include a filename.")
        printHelp()
        sys.exit()

    # Check that the user has supplied a valid input file (as last arg)
    inputFile = listArgs[-1]
    if (not path.exists(inputFile)):
        print("File {} doesn't exist ".format(inputFile))
        printHelp()
        sys.exit()

    # Currently we have options h for help, t to print tokens and labels,
    # and p to print parse tree
    unixOptions = "htp"
    gnuOptions = ["help", "tokenize", "parse-tree"]

    try:
        arguments, values = getopt.getopt(listArgs, unixOptions, gnuOptions)
    except getopt.error as err:
        # output error
        print(str(err))
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        if (currentArgument in ("-t", "--tokenize")):
            flag = flag | 1
        if (currentArgument in ("-p", "--parse-tree")):
            flag = flag | 10
        if (currentArgument in ("-h", "--help")):
            printHelp()
            sys.exit()
    try:
        f = open(inputFile, 'r')
    except OSError:
        print("ERROR: Could not open/read " + inputFile + ".")

    with f:
        # Read file, store the entire file in a string
        fileString = f.read()
    
    # Goes to the tokenizer
    lexer = tokenizer(fileString)
    # Get the symbolTable
    
    if (flag & 1 or flag == 0):
       # prints the tokens
        # printTokens(lexer)
        pass
    if (flag & 10):
        # goes to parser and print the ast 
        ast = parser(lexer)
        printAST(ast)
    st.print()
