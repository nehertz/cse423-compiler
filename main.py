import sys
import getopt
import re
from os import path
import time

def printHelp():
    print("usage: scanner.py [-t] [-p] filename")
    print("Scanner options and arguments: ")
    print("-t   :print the sequence of tokens and labels")
    print("-p   :print parse tree ")
    print("-h   :print the usage information")
    print("Default   :print option -t")


def group(*choices): return '(' + '|'.join(choices) + ')'
# This function was stolen from Python tokenizer module


def any(*choices): return group(*choices) + '*'
# This function was stolen from Python tokenizer module


def maybe(*choices): return group(*choices) + '?'
# This function was stolen from Python tokenizer module


def scanner(fileString):

    keywords = ['auto', 'else', 'register', 'union', 'do', 'goto', 'short', 'double',
                'long', 'typedef', 'continue', 'if', 'sizeof', 'unsigned', 'int', 'switch', 'char',
                'for', 'static', 'volatile', 'struct', 'case', 'extern', 'signed', 'while', 'const',
                'break', 'enum', 'return', 'void', 'default', 'float']
    # Regex to find strings
    re_str = re.compile("[a-zA-Z]*")
    # Regex to check if a string is a valid identifier
    # re_id = re.compile("[a-zA-Z0-9_]*")
    re_id = r"[a-zA-Z0-9_]*"
    
    # Regex to find numbers
    re_num = r"[0-9]*"
    # Regex to find special characters
    re_spec = r"[^a-zA-Z0-9\s]*"
    # Stolen from https://stackoverflow.com/questions/171480/regex-grabbing-values-between-quotation-marks
    re_string = r"([\"'])(?:(?=(\\?))\2.)*?\1"
    # Stoeln from https://stackoverflow.com/questions/16160190/regular-expression-to-find-c-style-block-comments
    re_bloc_comments = r"\/\*(\*(?!\/)|[^*])*\*\/"
    # Not copied :)
    line_comments = r"\/\/(.)*"

    # Regex to find arithmetic operators
    # re_arith = re.compile("+\-\*\/\%")
    # # Regex to find bitwise operators
    # re_bitwise = re.compile("(<<)|(>>)|(&)|(\|)|(\^)|(~)")
    # # Regex to find relational operators
    # re_compare = re.compile("(==)|(\!=)|(>=)|(<=)")
    # # Regex to find assignment operators
    # re_assign = re.compile(
    #     "(=)|(\+=)|(-=)|(\*=)|(/=)|(%=)|(<<=)|(>>=)|(&=)|(\^=)|(\|=)")
    # # Regex to find ';'
    # re_semi = re.compile("[;]")
    # # Regexes to find parens
    # re_lparen = re.compile("[(]")
    # re_rparen = re.compile("[)]")
    # # Regexes tp find brackets
    # re_lbrack = re.compile("[[]")
    # re_rbrack = re.compile("[]]")
    # # Regexes tp find curly brackets
    # re_lcurly = re.compile("[{]")
    # re_rcurly = re.compile("[}]")
    # # Regexes tp find angle brackets
    # re_langle = re.compile("[<]")
    # re_rangle = re.compile("[>]")


    magical_regex = re.compile(r"[^a-zA-Z0-9\s]|[a-zA-Z0-9_]*")

    # TODO: Make a more magical regex to implement order of operations for strings/comments/multi-char ops
    
    # print(fileString)
    # Remove trailing and leading whitespace for each line
    for lineNum, line in enumerate(fileString):
        fileString[lineNum] = line.strip()
        # fileString[lineNum] = line.strip('\t',' ')  # use this if we want to preserve newlines

        if fileString[lineNum]:  # only executes on non-empty strings
            # pattern matching can go here
            tokenlist = re.findall(magical_regex, fileString[lineNum])

            tokenlist = list(filter(None, tokenlist))
            print(tokenlist)


    print("in scanner")


def parser(fileString):
    print("In parser")


if __name__ == "__main__":
    t1 = time.time()
    cmdArgument = sys.argv
    listArgs = cmdArgument[1:]
    flag = 0  # flag that tells us which options are enabled

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
    t2 = time.time()
    print("time : {}".format(t2 - t1))
