from enum import Enum

class TokenName(Enum):
        # data-types
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
        comma = 22
        single_quot = 23
        double_quot = 24
        increment = 25
        decrement = 26