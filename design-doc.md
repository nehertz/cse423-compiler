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
    - Using getopt to collect command-line options (check number of arguments and assign flag by or-ing with bit representation of option)
    - Take filename from command line input (not an option)
    - Default option outputs tokens and labels
    - Read from file
    - Assign file contents to string
    - Use conditional statements to determine option(s) selected

- Scanner(string input):
    - Notes:
        - Assume file is in UNIX format
        - Initially remove trailing whitespace (not \n) and leading whitespace (\t)
        - Split string by \n
        - Assign useful regex sequences to variables
        - Loop through list of lines
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
                1. **whole number**
                2. decimal number
                3. bin, hex, etc. representation
            - Else:
                1. Equals sign
                2. Binary operator
                3. Unary operator
                4. Comparison operators (do not include < and >)
                5. Bitwise operators
                6. Semicolons
                7. Lparen
                8. Rparen
                9. Lbracket
                10. Rbracket
                11. Lcurly
                12. Rcurly
                13. Langle
                14. Rangle

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
            