import re
import sys
'''
Class containing all the conversion from one-type to another type conversion. Commenting is not performed on all the functions as they're obvious from their names. 
'''


class TypeConversion:
    
    def __init__(self):
        self.character = re.compile(r'\'.\'')
    
    def convertInt2Float(self, expr):
        s = expr + '.00'
        return s
    
    def convertInt2Char(self, expr):
        num = int(expr)
        num &= 0xFF
        return str(num)
    
    def convertInt2Short(self, expr):
        num = int(expr)
        num &= 0xFFFF
        return str(num)
    
    def convertInt2Double(self, expr):
        return self.convertInt2Float(expr)
    
    def convertInt2UInt(self, expr):
        if ('-'.find(expr)):
            num = int(expr)
            num += 2 ** 32
            num &= 0xFFFFFFFF
            return str(num)
        return str(int(expr) & 0xFFFFFFFF)
    
    def convertInt2Long(self, expr):
        return expr
    
    def convertInt2LongLong(self, expr):
        return expr
    
    def convertInt2ULong(self, expr):
        if ('-'.find(expr)):
            num = int(expr) 
            num += 2 ** 64
            num &= 0xFFFFFFFFFFFFFFFF
            return str(num) 
        return str(int(expr) & 0xFFFFFFFFFFFFFFFF)
    
    def convertInt2UShort(self, expr):
        if ('-'.find(expr)):
            num = int(expr)
            num += 2 ** 16
            num &= 0xFFFF
            return str(num)
        return str(int(expr) & 0xFFFF)
    
    def convertInt2UChar(self, expr):
        if ('-'.find(expr)):
            num = int(expr)
            num += 2 ** 8
            num &= 0xFF 
            return str(num)
        return str(int(expr) & 0xFF)

    def convertFloat2Int(self, expr):
        return str(int(float(expr)))
    
    def convertFloat2Char(self, expr):
        return str(int(float(expr)) & 0xFF)
    
    def convertFloat2Short(self, expr):
        return str(int(float(expr)) & 0xFFFF)
    
    def convertFloat2Double(self, expr):
        return expr
    
    def convertFloat2UInt(self, expr):
        expr = self.convertFloat2Int(expr) 
        return self.convertInt2UInt(expr)
    
    def convertFloat2Long(self, expr):
        expr = self.convertFloat2Int(expr)
        return self.convertInt2Long(expr)
    
    def convertFloat2LongLong(self, expr):
        expr = self.convertFloat2Int(expr)
        return self.convertInt2LongLong(expr)
    
    def convertFloat2ULong(self, expr):
        expr = self.convertFloat2Int(expr)
        return self.convertInt2ULong(expr)
    
    def convertFloat2UShort(self, expr):
        expr = self.convertFloat2Int(expr)
        return self.convertInt2UShort(expr)
    
    def convertFloat2UChar(self, expr):
        expr = self.convertFloat2Int(expr)
        return self.convertInt2UChar(expr)
    
    def convertChar2Int(self, expr):
        if (self.character.match(expr)):
            try:
                num = ord(expr)
                return str(num)
            except:
                print("ASCII value not found")
                sys.exit(1)
        return expr
    
    def convertChar2Float(self, expr):
        expr = self.convertChar2Int(expr)
        return self.convertInt2Float(expr)
    
    def convertChar2Short(self, expr):
        expr = self.convertChar2Int(expr)
        return self.convertInt2Short(expr)
    
    def convertChar2Double(self, expr):
        return self.convertChar2Float(expr)
    
    def convertChar2UInt(self, expr):
        expr = self.convertChar2Int(expr)
        return self.convertInt2UInt(expr)
    
    def convertChar2Long(self, expr):
        return self.convertChar2Int(expr)
    
    def convertChar2LongLong(self, expr):
        return self.convertChar2Int(expr)
    
    def convertChar2ULong(self, expr):
        expr = self.convertChar2Int(expr)
        return self.convertChar2Long(expr)
    
    def convertChar2UShort(self, expr):
        expr = self.convertChar2Int(expr)
        return self.convertInt2UShort(expr)
    
    def convertChar2UChar(self, expr):
        expr = self.convertChar2Int(expr)
        return self.convertInt2UChar(expr)

    
    def convertShort2Int(self, expr):
        num = int(expr)
        num &= 0xFFFFFFFF
        return str(num)
    
    def convertShort2Char(self, expr):
        num = int(expr)
        num &= 0xFF
        return str(num)
    
    def convertShort2Float(self, expr):
        num = int(expr)
        num &= 0xFFFFFFFF
        return str(num)+ '.00'
    
    def convertShort2Double(self, expr):
        num = int(expr)
        return str(num) + '.00'
    
    def convertShort2UInt(self, expr):
        return self.convertInt2UInt(expr)
    
    def convertShort2Long(self, expr):        
        return self.convertInt2Long(expr)
    
    def convertShort2LongLong(self, expr):
        return self.convertInt2LongLong(expr)
    
    def convertShort2ULong(self, expr):
        return self.convertInt2ULong(expr)
    
    def convertShort2UShort(self, expr):
        if ('-'.find(expr)):
            num = int(expr)
            num += 2 ** 16 
            num &= 0xFFFF
            return str(num)
        return expr
    
    def convertShort2UChar(self, expr):
        if ('-'.find(expr)):
            num = int(expr)
            num += 2 ** 8
            num &= 0xFF
            return str(num)
        return str(int(expr) & 0xFF)
    
    
    def convertDouble2Int(self, expr):
        num = int(float(expr))
        num &= 0xFFFFFFFF
        return str(num)
    def convertDouble2Char(self, expr):
        expr = self.convertDouble2Int(expr)
        return self.convertInt2Char(expr)
    
    def convertDouble2Short(self, expr):
        expr = self.convertDouble2Int(expr)    
        return self.convertInt2Short(expr)
    
    def convertDouble2Float(self, expr):
        return expr
    
    def convertDouble2UInt(self, expr):
        expr = self.convertDouble2Int(expr)
        return self.convertInt2UInt(expr)
    
    def convertDouble2Long(self, expr):
        num = int(float(expr))
        num &= 0xFFFFFFFFFFFFFFFF
        return str(num)
    
    def convertDouble2LongLong(self, expr):
        expr = self.convertDouble2Long(expr)
        return self.convertLong2LongLong(expr)
    
    def convertDouble2ULong(self, expr):
        expr = self.convertDouble2Long(expr)
        return self.convertLong2ULong(expr)
    
    def convertDouble2UShort(self, expr):
        expr = self.convertDouble2Short(expr)
        return self.convertShort2UShort(expr)
    
    def convertDouble2UChar(self, expr):
        expr = self.convertDouble2Int(expr)
        return self.convertInt2Char(expr)

    def convertUInt2Int(self, expr):
        if (num & 0x80000000) :
            num = (num & 0x7FFFFFFF) - (2 ** 32)
            return str(num)
        return str(num)
    
    def convertUInt2Char(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2Char(expr)
    
    def convertUInt2Short(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2Short(expr)

    def convertUInt2Double(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2Double(expr)
    
    def convertUInt2Float(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2Float(expr)
    
    def convertUInt2Long(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2Long(expr)
    
    def convertUInt2LongLong(self, expr):
        expr = self.convertUInt2LongLong(expr)
        return self.convertInt2LongLong(expr)
    
    def convertUInt2ULong(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2ULong(expr)
    
    def convertUInt2UShort(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2UShort(expr)
    
    def convertUInt2UChar(self, expr):
        expr = self.convertUInt2Int(expr)
        return self.convertInt2UChar(expr)

    def convertLong2Int(self, expr):
        return str(int(expr) & 0xFFFFFFFF)
    
    def convertLong2Char(self, expr):
        return str(int(expr) & 0xFF)
    
    def convertLong2Short(self, expr):
        return str(int(expr) & 0xFFFF)
    
    def convertLong2Double(self, expr):
        expr = self.convertLong2Int(expr)
        return self.convertInt2Double(expr)
    
    def convertLong2UInt(self, expr):
        expr = self.convertLong2Int(expr)
        return self.convertInt2UInt(expr)
    
    def convertLong2Float(self, expr):
        expr = self.convertLong2Int(expr)
        return self.convertInt2Float(expr)
    
    def convertLong2LongLong(self, expr):
        return str(int(expr) & 0xFFFFFFFFFFFFFFFF)
    
    def convertLong2ULong(self, expr):
        if ('-'.find(expr)):
            num = int(expr)
            num += 2 ** 64
            num &= 0xFFFFFFFFFFFFFFFF
            return str(num)
        return str(num)
    
    def convertLong2UShort(self, expr):
        expr = self.convertLong2Int(expr)
        return self.convertInt2UShort(expr)
    
    def convertLong2UChar(self, expr):
        expr = self.convertLong2Int(expr)
        return self.convertInt2UChar(expr)

    def convertLongLong2Int(self, expr):
        return str(int(expr) & 0xFFFFFFFF)
    
    def convertLongLong2Char(self, expr):
        return str(int(expr) & 0xFF)
    
    def convertLongLong2Short(self, expr):
        return str(int(expr) & 0xFFFF)
    
    def convertLongLong2Double(self, expr):
        expr = self.convertLongLong2Int(expr)
        return self.convertInt2Double(expr)
    
    def convertLongLong2UInt(self, expr):
        expr = self.convertLongLong2Int(expr)
        return self.convertInt2UInt(expr)
    
    def convertLongLong2Long(self, expr):
        return expr
    
    def convertLongLong2Float(self, expr):
        self.convertLongLong2Int(expr)
        return self.convertInt2Float(expr)
    
    def convertLongLong2ULong(self, expr):
        return self.convertLong2ULong(expr)
    
    def convertLongLong2UShort(self, expr):
        return self.convertLong2UShort(expr)
    def convertLongLong2UChar(self, expr):
        return self.convertLong2UChar(expr)
    
    def convertUShort2Int(self, expr):
        num = int(expr)
        if (num & 0x8000):
            num = (num & 0x7FFF) - (2 ** 16)
            return str(num & 0xFFFFFFFF)
        return str(num & 0xFFFFFFFF)
    
    def convertUShort2Char(self, expr):
        expr = self.convertUShort2Int(expr)
        return self.convertInt2Char(expr)
    
    def convertUShort2Short(self, expr):
        num = int(expr)
        if (num & 0x8000):
            num = (num & 0x7FFF) - (2 ** 16)
            return str(num & 0xFFFF)
        return str(num & 0xFFFF)
    
    def convertUShort2Double(self, expr):
        expr = self.convertUShort2Int(expr)
        return self.convertInt2Double(expr)
    
    def convertUShort2UInt(self, expr):
        return str(int(expr) &  0xFFFFFFFF)
    
    def convertUShort2Long(self, expr):
        expr = self.convertUShort2Int(expr)
        return self.convertInt2Long(expr)
    
    def convertUShort2LongLong(self, expr):
        expr = self.convertUShort2Int(expr)
        return self.convertInt2LongLong(expr)
    
    def convertUShort2ULong(self, expr):
        expr = self.convertUShort2Int(expr)    
        return self.convertInt2ULong(expr)
    
    def convertUShort2Float(self, expr):
        expr = self.convertUShort2Int(expr)
        return self.convertInt2Float(expr)
    
    def convertUShort2UChar(self, expr):
        expr = self.convertUShort2Int(expr)
        return self.convertInt2UChar(expr)

    def convertULong2Int(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2Int(expr)
    
    def convertULong2Char(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2Char(expr)
    
    def convertULong2Short(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2Short(expr)
    
    def convertULong2Double(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2Double(expr)
    
    def convertULong2UInt(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2Int(expr)
    
    def convertULong2Long(self, expr):
        num = int(expr)
        if (num & 0x8000000000000000):
            num = (num & 0x7FFFFFFFFFFFFFFF) - (2 ** 64)
            return str(num & 0xFFFFFFFFFFFFFFFF)
        return str(num & 0xFFFFFFFFFFFFFFFF)
    
    def convertULong2LongLong(self, expr):
        return self.convertULong2Long(expr)
    
    def convertULong2Float(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2Float(expr)

    def convertULong2UShort(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2UShort(expr)
    
    def convertULong2UChar(self, expr):
        expr = self.convertULong2Long(expr)
        return self.convertLong2UChar(expr)

    def convertUChar2Int(self, expr):        
        if (self.character.match(expr)):
            try:
                num = ord(expr)
                return str(num)
            except: 
                print("ASCII value not found")
                sys.exit(1)
        else:
            return expr
    def convertUChar2Char(self, expr):
        if (self.character.match(expr)):
            try:
                num = ord(expr)
                return str(num)
            except:
                print("ASCII value not found")
                sys.exit(1)
        else: 
            num = int(expr)
            if (num & 0x80):
                num = (num & 0x7F) - (2 ** 8)
                return str(num) 
            return str(num)
        return 
    
    def convertUChar2Short(self, expr):
        return self.convertUChar2Int(expr)
    
    def convertUChar2Double(self, expr):
        expr = self.convertUChar2Int(expr)
        return self.convertInt2Double(expr)
    
    def convertUChar2UInt(self, expr):
        if (self.character.match(expr)):
            try:
                num = ord(expr)
                return str(num)
            except:
                print("ASCII Value Not found")
                sys.exit(1)
        return expr
    
    def convertUChar2Long(self, expr):
        return self.convertUChar2Int(expr)
    
    def convertUChar2LongLong(self, expr):
        return self.convertUChar2Int(expr)
    
    def convertUChar2ULong(self, expr):
        return self.convertUChar2UInt(expr)
    
    def convertUChar2UShort(self, expr):
        return self.convertUChar2UInt(expr)
    
    def convertUChar2Float(self, expr):
        return self.convertUChar2Double(expr)