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
* -h : print the usage information
* -t : print the sequence of tokens and labels 
* -p : print parse tree 
* -s : print symbol table
* -i : print IR
* -o : write IR into a file
* -r : read IR from a file

# How to use option -o
```
python3 main.py -o source_filename output_filename
```
# How to use option -r
```
python3 main.py -r filename
```


