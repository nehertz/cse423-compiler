# C Subset Compiler
## Built for CSE 423: Compiler Writing

### Nathan Hertz
### Wing Lin
### Yash Shah
### Andy Xiang

# Overview
This goal of this project is to create a compiler for a subset of the C programming language, which will translate that subset of C into assembly language. The project will be written in Python.

# Existing Solution
1. Read from file
2. Scan and tokenize input using lex (PLY Project)
3. Parse tokenized input using yacc (PLY Project)
4. Convert parsed input into parse tree format using skbio

## Working Features
KEY | | |
--- | --- | ---
[--] Not implemented | [X] Implemented | [/] Partially implemented

**Required:**
- [X] Identifiers
- [X] Variables
- [X] Functions
- [X] Keywords
- [X] Arithmetic expressions
- [X] Assignment
- [X] Boolean expressions
- [X] Goto statements
- [X] If/else control flow: One-line loops/conditionals aren't currently supported
- [X] Unary operators (unary minus (`-`), NOT (`!`), `sizeof()`)
- [X] Return statements
- [/] Break statements: Break can currently be placed outside of loops and switches
- [X] While/do-while loops: One-line loops/conditionals aren't currently supported

**Optional:**
- [X] Floats
- [X] Characters
- [X] ++/--/-=/+=/*=//=
- [X] For loops: One-line loops/conditionals aren't currently supported
- [X] Binary operators
- [X] Switch statements

**Not expected, but may be attempted:**
- [--] Pointers
- [--] Arrays
- [/] Strings: Strings are being scanned but are not parsed due to our lack of pointer support
- [/] Preprocessor statements: Only currently support `#include <file.h>` and `#include "file.h"`
- [/] Struct/union: Structs/unions can be defined but accessing elements of a struct/union is not supported
- [ ] Enum
- [ ] Casting/type promotion
- [X] Type specs

# Design Discussion
- Command line user input (in main):
    - Using getopt to collect command-line options (check number of arguments and assign flag by or-ing with bit representation of option)
    - Take filename from command line input (not an option)
    - Default option outputs tokens and labels
    - Read from file
    - Assign file contents to string
    - Use conditional statements to determine option(s) selected

- Scanner(string input):
    - Implemented using lex from the PLY Project
    - Acceptable tokens are defined and compiled into single 'tokens' list
    - Ignored input characters are specified
    - For each token, a function is defined
        - Function identifies a token based on a given regex
        - Token may be further modified using Python code
    - tokenizer() function calls the appropriate PLY functions and returns the labeled token list

- Parser:
    - Implemented using yacc from the PLY Project
    - For each grammar rule, a function is defined
        - The grammar rule takes in a Python docstring with the rule specified within (syntax: ''' ruleName : rule1 | rule2 ''')
        - Below, Python code is used to format the parsed input (to be placed into the AST)
    - Additionally, a start symbol and error function are defined
        - The error function is called whenever the parser runs into input that is not handled by a grammar rule; returns the value and line number of the token that threw the error
    - parser() calls the appropriate PLY functions that parse the output based on the defined grammar rules and returns
    - The output is formatted into an AST using skbio
- Symbol Table
- Type checking (Obtaines the Tasks from: https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-035-computer-language-engineering-spring-2010/lecture-notes/MIT6_035S10_lec06.pdf)
    - Number of arguments matches the number of formals and the corresponding types are equivalent
    - If called as an expression, should return a type
    - Each access of a variable should match the declaration (arrays, structures, etc.) 
    - Identifiers in an expression should be "evaluatable"
    - LHS of an assignment should be "assignable"
    - In an expression all the types of variables, method return types and operators should be "compatible"
    - Type Promotion and Demotion:
        - When LHS has a higher type than the RHS, the RHS type will be promoted always. We perform type promotion with only specific types.
        - When LHS has a lower type than the RHS, the truncation or type demotion will happen. We perform type demotion with only specific types. 
        - Type prmotion and type demotion are performed with a following types
        (+ve = type promotion and -ve = type demotion)
            - lvalue: INT
                - rvalue: LONG (-ve)
                - rvalue: float (conversion if a NUMCONST Not on ID)
                - rvalue: unsigned int (conversion)
                - rvalue: 



# Known Errors
- Our grammar will throw shift/reduce conflict warnings occasionally; we are working on fixing them