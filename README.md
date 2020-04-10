# CSE423 Compiler Writing 

* Nathan Hertz (github ID: nehertz)
* Yash Shah (github ID: ys9)
* Wing Ho Lin (github ID: Wing Lin)
* Anhao Xiang (github ID: AndyXiang945)

# How to install Python dependencies

* Run this in your terminal: Tested on Ubuntu bionic

```
pip3 install -r documentation/requirements2.txt
```

# How to Use
```
python3 main.py -options filename
```
* options: 
* -h : print the usage information
* -t : print the sequence of tokens and labels 
* -p : print parse tree 
* -s : print symbol table
* -i : print IR
* -o : write IR into a file
* -r : read IR from a file
* -m : turn on the optimization pass(in progress)
* -a : output assembly(in progress)

# test1.c in the main directory contains all the test cases we used. 

# How to use option -o
```
python3 main.py -o source_filename output_filename
```
# How to use option -r
```
python3 main.py -r filename
```
# How to use option -m
```
To print the optimized IR: 
python3 main.py -i -m filename
```
```
To print the optimized assembly: 
python3 main.py -a -m filename
```

