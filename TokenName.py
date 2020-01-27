from enum import Enum

class TokenName(Enum):
        TypeSpecifier = 1
        String = 2 
        Identifier = 3 
        NumberConstant = 4 
        SpecialCharacter = 5 
        BitwiseOperator = 6
        ComparisonOperator = 7 
        Equals = 8 
        Semicolon = 9
        LParen = 10
        RParen = 11
        LBracket = 12
        RBracket = 13 
        LCurly = 14
        RCurly = 15 
        LAngle = 16
        RAngle = 17
        ArithmeticOperator = 18
        Keyword = 19
        LogicalOperator = 20
        AssignmentOperator = 21
        Comma = 22
        SingleQuot = 23
        DoubleQuot = 24
        Increment = 25
        Decrement = 26
        Colon = 27