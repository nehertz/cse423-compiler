# CSE423 Compiler Writing 

* Nathan Hertz (github ID: nehertz)
* Yash Shah (github ID: ys9)
* Wing Ho Lin (github ID: Wing Lin)
* Anhao Xiang (github ID: AndyXiang945)

# How to install Python dependencies

* Run this in your terminal: Tested on Ubuntu bionic

```
pip3 install -r documentation/requirements.txt
```

# How to Use
```
python3 main.py -options filename
```
* options: 
* -t : print the sequence of tokens and labels 
* -p : print parse tree 
* -s : print symbol table
* -i : print IR
* -o : write IR into a file
* -r : read IR from a file
* -m : turn on the optimization pass
* -a : print assembly code with efficient register allocation algorithm 
* -b : print assembly code with inefficient register allocation algorithm 
       some test-cases are problematic when using the -b option(inefficient allocation algorithm)
* -a -m : print the efficient assembly code with optimization turn on 
* -b -m : print the inefficient assembly code with optimization turn on 
* -i -m : print the IR with optimization turn on 
* -r -a : read the IR from a file, and print the assembly code
* -h : print the usage information


# test1.c in the main directory contains all the test cases we used. 

# How to use option -o
```
python3 main.py -o source_filename output_filename
```
# How to use option -r
```
Read IR from a file and print the IR
python3 main.py -r filename
```

```
Read IR from a file and print the assembly code
python3 main.py -r -a filename
```
# How to use option -m
```
To print the optimized IR: 
python3 main.py -i -m filename
```

```
To print the optimized assembly: 
python3 main.py -a -m filename
or
python3 main.py -b -m filename

Note: Turning on -a option, the assembly code generation will utilize
an effcient register allocatoin algorithm. Turning on -b option, an ineffcient algorithm will be used.
```



