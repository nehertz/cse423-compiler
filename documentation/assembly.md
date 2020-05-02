Assembly TO-Do List:
 - Create a dictionary that keeps track of variables - and addresses. 
 - Keep track of registers
 - Var assignment with expression - Andy
 - goto- statements - Yash
 - conditionals - Nathan 
 - loops - Wing
 - func-call - Yash
To Research:  Register allocation algorithm
We're doing 64-bit registers at&t syntax
- Symbol Table memory fetcher: 
    - 

Notes:
- Three parts to the back end:
    1. Instruction selection: the process of choosing which x86 instructions will be represented by each component of the linear IR (e.g. a = b + c -> addq \<b-loc> \<c-loc>)
        - In x86, there are lots of different ways to do the same thing (e.g. to zero out a register, you could XOR it or subtract it by itself, etc.)
        - Better to narrow down to one good solution for each action for simplicity
    2. Instruction scheduling: the process of optimizing instructions based on hardware (e.g. performing adds/mults/ in parallel, performing other actions during "downtime", etc.)
        - **Not required for our compiler!**
    3. Register allocation: allocation of program variables to CPU registers
        - We need a representation of all the registers within our compiler, including which registers are used for which instructions and which can be used freely for storage
        - For each instruction, take the set of available registers and figure out how to map the variables that we have to the available registers

- x86 instructions we will need to support:
- **We don't need to add size suffix to instructions (e.g. `movl`, `movq`); GCC will figure it out based on the registers and memory used**
- AT&T Syntax:
    - **`instr <src>,<dest>`**\
    - `$const` e.g. `$42`
    - `%reg` e.g. `%eax`
    - mem location: `const(%reg)` e.g. `-12(%esp)`
    - Be careful when looking up documentation that it is formatted in AT&T syntax
- Move:
    - `mov <reg>,<reg>`
    - `mov <reg>,<mem>`
    - `mov <mem>,<reg>`
    - `mov <const>,<reg>`
    - `mov <const>,<mem>`
- Push:
    - `push <reg32>`
    - `push <mem>`
    - `push <const32>`
- Pop:
    - `pop <reg32>`
    - `pop <mem>`
- Add:
    - `add <reg>,<reg>`
    - `add <reg>,<mem>`
    - `add <mem>,<reg>`
    - `add <const>,<reg>`
    - `add <const>,<mem>`
- Subtract:
    - `sub <reg>,<reg>`
    - `sub <reg>,<mem>`
    - `sub <mem>,<reg>`
    - `sub <const>,<reg>`
    - `sub <const>,<mem>`
- Shift:
    - `shl <con8>, <reg>`
    - `shl <con8> ,<mem>`
    - `shl <cl>, <reg>`
    - `shl <cl>, <mem>`

    - `shr <con8>, <reg>`
    - `shr <con8>, <mem>`
    - `shr <cl>,<reg>`
    - `shr <cl>, <mem>`
- Multiplication:
    - Destination must be a register
    - `imul <reg32>,<reg32>`
    - `imul <mem>,<reg32>`
- Division:
    - Divides against 64-bit `%edx`:`%eax` (\<most sign. bits>:\<least sign. bits>), with result in `%eax` and remainder in `%edx`
    - If you want to divide a 32-bit value, simply clear out `%edx` and place value in `%eax`
    - `idiv <reg32>`
    - `idiv <mem>`
- and, or, xor: 
    - `and/or/xor <reg>, <reg>`
    - `and/or/xor <mem>, <reg> `
    - `and/or/xor <reg>, <mem> `
    - `and/or/xor <con>, <reg> `
    - `and/or/xor <con>, <mem> `

- Comparisons:
    - Sets flags based on the result of the comparison
    - `cmp <reg>,<reg>`
    - `cmp <reg>,<mem>`
    - `cmp <mem>,<reg>`
    - `cmp <const>,<reg>`
- Jumps:
    - `jmp <label>` (unconditional jump)
    - `je <label>` (jump if equal)
    - `jne <label>` (jump if not equal)
    - `jz <label>` (jump if last result was zero)
    - `jg <label>` (jump if greater than)
    - `jge <label>` (jump if greater than or equal)
    - `jl <label>` (jump if less than)
    - `jle <label>` (jump if less than or equal)