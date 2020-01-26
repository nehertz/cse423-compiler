import sys
import getopt
import re
from os import path
import time
from io import BytesIO
from scanner import *


def printHelp():
    print("usage: scanner.py [-t] [-p] filename")
    print("Scanner options and arguments: ")
    print("-t   :print the sequence of tokens and labels")
    print("-p   :print parse tree ")
    print("-h   :print the usage information")
    print("Default   :print option -t")


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
    # Read file, store the entire file in a string
    try:
        f = open(inputFile, 'r')
    except OSError:
        print("ERROR: Could not open/read " + inputFile + ".")

    with f:
        fileString = f.read()

    if (flag & 1 or flag == 0):
        # goes to scanner and prints the tokens
        tokens = scan(fileString)
        tokenize(tokens)
    #if (flag & 10):
        # goes to parser
        # parse(fileString)