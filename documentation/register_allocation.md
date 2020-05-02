Following 8-byte registers are used:
    - %rax
    - %rcx
    - %rdx
    - %rbx
    - %rsi
    - %rdi 
    - %rsp
    - %rbp
    - %r8
    - %r9
    - %r10
    - %r11
    - %r12
    - %r13
    - %r14
    - %r15

Instructions:
    - mov S, D :S, D could be memory or register
    - push S: S =register
    - pop D: D = register, memory
    
Register Allocation algorithm using Interference Graph:
Resource: https://www.cs.cmu.edu/~fp/courses/15411-f14/lectures/03-regalloc.pdf
    This algorithm makes use of dynamic programming
    - in which we go through the code in reverse order, line-by-line and find the live-variables in the line. The definition of live variable is as follows:
    The variable is live at a given program point if it will be used in the remainder of the computation. Therefore, basically two live-variables having an overlapping live-ranges can not overlap, because they may both be then used at the same time.

    - interference graph is a graph whose nodes are variables and registers of the program. There is an undirected edge between two nodes if the corresponding variables interfere and should be assigned to different registers. There are never edges from a node to itself, because, at any particular use, variable x is put in the same register as variable x. 

    - Register allocation from live-ness analysis: We use graph coloring and especially greedy coloring algorithm for register allocation. The registers are colors and we color all the nodes by making sure that no-neighboring nodes have the same color. 

    - Register spilling: 
    Register spilling is done when we don't have enough registers to store all the live-variables in a particular range. Currently we don't support register spilling due to time-restraint. For small programs, when less than 10 variables are interacting with each other simultaneously, register spilling is not necessary. 

    - Precolored Nodes:
    We perform precoloring for certain operation. For example, idiv instruction makes use of %rax, and %rdx; ret instruction makes use of %rax. We draw an edge to the register when this instructions are live. 

Basic Register Allocation Algorithm:

    - Basic register allocation is simple, but very inefficient and therefore shouldn't really be used. 