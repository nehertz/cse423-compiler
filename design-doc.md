# C Subset Compiler
## Built for CSE 423: Compiler Writing

### Nathan Hertz
### Wing Lin
### Yash Shah
### Andy Xiang

# Overview -
This goal of this project is to create a compiler for a subset of the C programming language, which will translate that subset of C into assembly language. The project will be written in Python.

# Milestones
Start date: January 13, 2020

- Milestone 1 - Begin work on parser: TBD
- Milestone 2 - Complete parser: TBD

Due date: April 2X, 2020? Don't know exact date.

# Existing Solution
1. Read from file
2. Parse input
3. Tokenize parsed input
4. Convert tokenized input into parse tree

# Design Discussion
- Command line user input (in main):
    - [x] Using getopt to collect command-line options (check number of arguments and assign flag by or-ing with bit representation of option)
    - [x] Take filename from command line input (not an option)
    - [x] Default option outputs tokens and labels
    - [x] Read from file
    - [x] Assign file contents to string
    - [x] Use conditional statements to determine option(s) selected

- Scanner(string input):
    - Notes:
        - Assume file is in UNIX format
        - [x] Initially remove trailing whitespace and leading whitespace
        - [x] Assign useful regex sequences to variables
        - [x] Loop through list of lines
        1. Loop through line character-by-character:
            - Advantages: Simple, maybe, kinda brute force
            - Disadvantages: Slow and annoying
        2. Check line with regexes to determine if its a string, number, or special character:
            - Pros: elegant, most likely faster
            - Cons: more regexes :(
        - Now we have list of tokens
        - Assign each token its label within a list of tuples:
            - Regex determines if token is sequence of alphanumeric characters:
                - Keyword
                - Identifier
            - Regex determines if token is sequence of numeric characters:
                1. [x] **whole number**
                2. decimal number
                3. bin, hex, etc. representation
            - Else:
                1. [x] Equals sign
                2. [x] Binary operator
                3. [x] Unary operator
                4. [x] Comparison operators (do not include < and >)
                5. [x] Bitwise operators
                6. [x] Semicolons
                7. [x] Lparen
                8. [x] Rparen
                9. [x] Lbracket
                10. [x] Rbracket
                11. [x] Lcurly
                12. [x] Rcurly
                13. [x] Langle
                14. [x] Rangle

        - Output list of tuples

- Parser:
    - Error checking for valid C syntax:
        1. ~~Pre-processor shenanigans (include statements, etc.)~~
        2. Global variables
        3. Functions
            - Variable declaration
            - Variable declaration and definition
            - Existing variable definition
            - While loops
            - ~~For loops~~
            - Conditionals
            - ~~Switch~~
            - Goto statements
            - Continue/break
            - Function calls
            - Return statements
            