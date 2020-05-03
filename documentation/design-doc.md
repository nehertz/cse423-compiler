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
5. Using the parse tree to construct symbol table
6. Conduct type checking 
7. Convert parse tree(ast) into linear IR
8. provide options to read IR from a file or output the IR to a file

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
- [X] If/else control flow: One-line loops/conditionals aren't currently supported, 
- [/] Unary operators (unary minus (`-`), NOT (`!`), `sizeof()`)
- [X] Return statements
- [X] Break statements
- [X] While/do-while loops: One-line loops/conditionals aren't currently supported

**Optional:**
- [X] Floats
- [--] Characters
- [X] ++/--/-=/+=/*=//=
- [X] For loops: One-line loops/conditionals aren't currently supported
- [X] Binary operators
- [--] Switch statements

**Not expected, but may be attempted:**
- [--] Pointers
- [--] Arrays
- [--] Strings: Strings are being scanned but are not parsed due to our lack of pointer support
- [--] Preprocessor statements: Only currently support `#include <file.h>` and `#include "file.h"`
- [--] Struct/union: Structs/unions can be defined but accessing elements of a struct/union is not supported
- [--] Enum 
- [--] Casting/type promotion : Supported after type_checking. But not in the C program.
- [--] Type specs

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
    - Implemented using the class SymbolTable which contains the list of tuples with the following
        - name of the token
        - type of the token
        - an actual scope of the token (calculations are shown in the SymbolTable.py)
        - abstract scope of the token (i.e. token belongs to which function)
    - Implemented an auxiliary class which helps with  function arguments, return type, etc.
        - class is called functionDS.py
        - That class includes a method to check the right number and right types of the arguments
            later in type_checking.py
        - This function unites both SymbolTable.py and typeChecking.py in their functions
    - Generation of SymbolTable
        - Generation of Symbol Table occurs along with  Parser. 
        - When function declaration occurs:
            - FunctionDS instant is created which is maintained in a list
            - The number of arguments are read using embedded action functionality of Python PLY (https://www.dabeaz.com/ply/ply.html#ply_nn35b) This is being used along with the dummy grammar i.e. parametersBegin and parametersEnd. This way of dummy grammar is associated with particular action done on symbol table i.e. when parametersBegin is encountered, symbolTable will record every variable declaration as a parameter until parametersEnd is encountered. All the encountered parameters are included in FunctionDS instance of a respectivve function.
        - when any ID is encountered withing a program
            - it is being looked up using the respective scope.
                - the advantage of doing this is we will not have to calculate the scope as the parse performs this line-by-line and scope is maintained. 
    - Usage of SymbolTable 
        - Usage of SymbolTable is very useful in typeChecking
            - here we make use of abstracted scope functionality of the symbol table as the scope-checking has already been done in the previous phases. 
            - Abstract scope gives information about what function the variable is in
                - i.e. if there are only 2 functions defined in the program and you want to access the variable's scope from the second function, then the scope will be 2. This calculation IGNORES nestedScope function of the Symbol Table

- Type_checking
    - Implemented using the class TypeChecking which performs the following tasks
        - Checks type of every assignment, expression. We support following of assignment and expression.
            - 2 types of assignment : when rvalue is function-call and when r-value is expression
            - expression can be inside of function as a parameter and we will still be able to perform type-casting on it
            - expression can be inside of while-loop, for-loop, if-else statement
        - When function-call is performed, it checks for the following:
            - number of parameters passed
            - type of parameter
            - return type of function - matching with l-value. 
        - Type casting if variable is not of appropriate type
            - we perform type-promotion and/or demotion based upon the type of l-value. We always convert the ID type if it doesn't match with l-value's type.
            - Type-casting occurs for func-calls as well. If the return type is not same as l-value, then type-casting will occur.
        - Type casting is supported for following types:
            - int, float, long, long long, double, char, short with both signed and unsigned version. 
        - Type conversion for NUMCONST use-cases
            - two major type-conversion occurs, int -> float and float -> int. If r-value is 12 and l-value has a type of float/double then type-conversion will
            occur i.e. number 12 will be changed to 12.00; Therefore, typeChecking makes changes to ast.

- IR 
    - IR is implemented using abstract syntax tree. While traversing the tree by level-order, we pass the node to different IR converting functions.
    - In order to achieve this, we have modified the AST so that each statement will have a distinct parent. For example, the AST of varable declration statment will have parent 'varDecl', and the AST of variable assignment will have parent 'varAssign' etc. In this way, we can recognized where we are in the AST, and to help us to decide which function we need pass the node to.  
    - Different converting functions such as assign(), and args() and etc, will traverse the AST subtree which the subtree root will be passed in function parameter. Then, append the converted IR into IR data structure call self.IRS.   
    - For more deatils, design of the IR converting process follows the structure of AST. run() function in IR class scanns the first level of AST, wihch this level should contains: 
        - Function name 
        - Global variable
        - enum
    - When any node is recognized, it will be passed to corresponding functions and its children will be further converted
    - funcNode() is one major function which handles IR conversion of: 
        - function name
        - function arguments
        - function statements
    - Majority of the function conversion takes place at function-statement. Which is handled by statement() function. 
    - statement() function traverse the children of statement node and passed the children to other converting function: 
        - Assignment statement 
        - var decl/assign 
        - function calls 
        - enum
        - goto statement
        - if statement 
        - iteration statements
    - We decide to adopt this approach because using different function to handle the conversion job of different node types makes sense when traversing the tree structure. And one conversion function such as statement() can be re-used in many other functions such as when converting for-loop, we only need to worry about converting for-loop conditions, and pass the statement node under for-loop branch to statement() function. In this way, placing IR at correct location is also guaranteed.   
    
- Assembly code generation
    - The code generation is implemented using the IR. We take the IR list as input and scan through each line of the IR. Each line will be determined and passed to corresponding functions that handles the code generation. We utiliz a list structure to store the final output of assembly code, assembly codes will be apended to the list while scanning through each line of IR. Therefore we can keep the order. 
    - We only support a subset of x86-64 instruction, which are included in assembly.md file. 
    - For the register allocation, we support two different types of allocation. the details are in register_allocation.md

# Known Errors
- Our grammar will throw shift/reduce conflict warnings occasionally; we are working on fixing them