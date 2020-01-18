import sys
import getopt
import re
from os import path

def printHelp():
        print("usage: scanner.py [-t] [-p] filename")
        print("Scanner options and arguments: ")
        print("-t   :print the sequence of tokens and labels")
        print("-p   :print parse tree ")
        print("-h   :print the usage information")
        print("Default   :print option -t")


def scanner(fileString):

        keywords = ['auto', 'else', 'register', 'union', 'do', 'goto', 'short', 'double',
        'long', 'typedef', 'continue', 'if', 'sizeof', 'unsigned', 'int', 'switch', 'char',
        'for', 'static', 'volatile', 'struct', 'case', 'extern', 'signed', 'while', 'const',
        'break', 'enum', 'return', 'void', 'default', 'float']        
        # Regex to find strings
        re_str = re.compile("[a-zA-Z]*")
        # Regex to check if a string is a valid identifier
        re_id = re.complie("[a-zA-Z0-9_]*")
        # Regex to find numbers
        re_num = re.compile("[0-9]*")
        # Regex to find special characters
        re_spec = re.compile("[^a-zA-Z0-9\s]*")
        # Regex to find arithmetic operators
        re_arith = re.compile("+\-\*\/\%")
        # Regex to find bitwise operators
        re_bitwise = re.compile("(<<)|(>>)|(&)|(\|)|(\^)|(~)")
        # Regex to find relational operators
        re_compare = re.compile("(==)|(\!=)|(>=)|(<=)")
        # Regex to find assignment operators
        re_assign = re.compile("(=)|(\+=)|(-=)|(\*=)|(/=)|(%=)|(<<=)|(>>=)|(&=)|(\^=)|(\|=)")
        # Regex to find ';'
        re_semi = re.compile("[;]")
        # Regexes to find parens
        re_lparen = re.compile("[(]")
        re_rparen = re.compile("[)]")
        # Regexes tp find brackets
        re_lbrack = re.compile("[[]")
        re_rbrack = re.compile("[]]")
        # Regexes tp find curly brackets
        re_lcurly = re.compile("[{]")
        re_rcurly = re.compile("[}]")
        # Regexes tp find angle brackets
        re_langle = re.compile("[<]")
        re_rangle = re.compile("[>]")
        

        print(fileString)
        
        # Remove trailing and leading whitespace for each line
        for lineNum, line in enumerate(fileString):
                fileString[lineNum] = line.strip()
                #fileString[lineNum] = line.strip('\t',' ')  # use this if we want to preserve newlines

                if fileString[lineNum]:  # only executes on non-empty strings
                        # pattern matching can go here
                        
                                
                                
                
        # Removes an empty string i.e. the lines which were empty
        # fileString = list(filter(None, fileString))
        # fileString[:] = [x for x in fileString if x]
        
        
        
        print("in scanner")










def parser(fileString):
        print("In parser")

if __name__== "__main__":
        cmdArgument = sys.argv 
        listArgs = cmdArgument[1:]
        flag = 0 # flag that tells us which options are enabled
        
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
        # Read file, store the entire file in a string
        try:
                f = open(inputFile, 'r')
        except OSError:
                print("ERROR: Could not open/read " + inputFile + ".")
        
        with f:
                fileString = f.readlines()
        
        if (flag & 1 or flag == 0):
                # goes to scanner and prints the tokens 
                scanner(fileString)
        if (flag & 10):
                # goes to parser 
                parser(fileString)
