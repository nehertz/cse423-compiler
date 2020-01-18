# C Tokens

# Key Words -

||||||
|-|-|-|-|-|
| auto     | double   | int      | struct | break   |
| else     | long     | switch   | case   | enum    |
| register | typedef  | char     | extern | return  |
| union    | continue | for      | signed | void    |
| do       | if       | static   | while  | default |
| goto     | sizeof   | volatile | const  | float   |
| short    | unsigned |          |        |         |

# Identifiers -
* An identifier can only have alphanumeric characters (a-z , A-Z , 0-9) (i.e. letters & digits) and underscore( _ ) symbol.
* Identifier names must be unique
* The first character must be an alphabet or underscore.
* Only first thirty-one (31) characters are significant.
* Must not contain white spaces.
* Identifiers are case-sensitive.

# Constant -
* Numeric Constants
    * Integer Constant 
        * Decimal Integer
        * Octal Integer
        * Hexadecimal Integer
    * Real Constant 
* Character Constants
    * Single Character Constants 
    * String Constants 
    * Backslash Character Constants 

| Constants | Meanings        |
|-----------|-----------------|
| \a        | Beep            |
| \b        | Backspace       |
| \f        | form feed       |
| \n        | new line        |
| \r        | carriage return |
| \t        | horizontal tab  |
| \v        | vertical tab    |
| \'        | single quote    |
| \"        | double quote    |
| \\        | backslash       |
| \0        | null            |

# Operators -
* Arithmetic

| Operator | Description     |
|----------|-----------------|
| +        |  Addition       |
| -        |  Subtraction    |
| *        |  Multiplication |
| /        |  Division       |
| %        |  Modulus        |

* Relational

| Operator | Description              |
|----------|--------------------------|
| ==       | Is equal to              |
| !=       | Is not equal to          |
| >        | Greater than             |
| <        | Less than                |
| >=       | Greater than or equal to |
| <=       | Less than or equal to    |

* Logical

| Operator | Description |
|----------|-------------|
| &&       | AND         |
| \|\|     | OR          |
| !        | NOT         |

* Assignment

| Operator | Description                     |
|----------|---------------------------------|
| =        | Assign                          |
| +=       | Increments then assign          |
| -=       | Decrements then assign          |
| *=       | Multiplies then assign          |
| /=       | Divides then assign             |
| %=       | Modulus then assign             |
| <<=      | Left shift and assign           |
| >>=      | Right shift and assign          |
| &=       | Bitwise AND assign              |
| ^=       | Bitwise exclusive OR and assign |
| \|=       | Bitwise inclusive OR and assign |

* Increment and Decrement

| Operator  | Description     |
|-----------|-----------------|
| ++        |  Increment      |
| --        |  Decrement      |

* Conditional

| Operator | Description            |
|----------|------------------------|
| ?:       | Conditional Expression |

* Bitwise

| Operators | Description                     |
|-----------|---------------------------------|
| <<        | Binary Left Shift Operator      |
| >>        | Binary Right Shift Operator     |
| ~         | Binary Ones Complement Operator |
| &         | Binary AND Operator             |
| ^         | Binary XOR Operator             |
| \|         | Binary OR Operator              |

* Special 

| Operator | Description                       |
|----------|-----------------------------------|
| sizeof() | Return Size of a memory location  |
| &        | return address of memory location |

# Special Symbols -

| Symbols | Description                            |
|---------|----------------------------------------|
| [ ]     | Array element reference                |
| ( )     | Function calls and function parameters |
| < >     | ...                                    |
| { }     | start and end of a block of code       |
| ,       | separate more than one statements      |
| ;       | end of a statement                     |
| *       | Pointer                                |