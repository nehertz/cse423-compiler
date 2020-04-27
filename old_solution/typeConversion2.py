import re
import sys

conversion = {}

def add_conversion(key):
    def _add_conversion(func):
        conversion[key] = func
        return func
    return _add_conversion




character = re.compile(r'\'.\'')

# @add_conversion('convertInt2Float'
def convertInt2Float( expr):
    s = expr + '.00'
    return s

def convertInt2Char( expr):
    num = int(expr)
    num &= 0xFF
    return str(num)

def convertInt2Short( expr):
    num = int(expr)
    num &= 0xFFFF
    return str(num)

def convertInt2Double( expr):
    return convertInt2Float(expr)

def convertInt2UInt( expr):
    if ('-'.find(expr)):
        num = int(expr)
        num += 2 ** 32
        num &= 0xFFFFFFFF
        return str(num)
    return str(int(expr) & 0xFFFFFFFF)

def convertInt2Long( expr):
    return expr

def convertInt2LongLong( expr):
    return expr

def convertInt2ULong( expr):
    if ('-'.find(expr)):
        num = int(expr) 
        num += 2 ** 64
        num &= 0xFFFFFFFFFFFFFFFF
        return str(num) 
    return str(int(expr) & 0xFFFFFFFFFFFFFFFF)

def convertInt2UShort( expr):
    if ('-'.find(expr)):
        num = int(expr)
        num += 2 ** 16
        num &= 0xFFFF
        return str(num)
    return str(int(expr) & 0xFFFF)

def convertInt2UChar( expr):
    if ('-'.find(expr)):
        num = int(expr)
        num += 2 ** 8
        num &= 0xFF 
        return str(num)
    return str(int(expr) & 0xFF)

def convertFloat2Int( expr):
    return str(int(float(expr)))

def convertFloat2Char( expr):
    return str(int(float(expr)) & 0xFF)

def convertFloat2Short( expr):
    return str(int(float(expr)) & 0xFFFF)

def convertFloat2Double( expr):
    return expr

def convertFloat2UInt( expr):
    expr = convertFloat2Int(expr) 
    return convertInt2UInt(expr)

def convertFloat2Long( expr):
    expr = convertFloat2Int(expr)
    return convertInt2Long(expr)

def convertFloat2LongLong( expr):
    expr = convertFloat2Int(expr)
    return convertInt2LongLong(expr)

def convertFloat2ULong( expr):
    expr = convertFloat2Int(expr)
    return convertInt2ULong(expr)

def convertFloat2UShort( expr):
    expr = convertFloat2Int(expr)
    return convertInt2UShort(expr)

def convertFloat2UChar( expr):
    expr = convertFloat2Int(expr)
    return convertInt2UChar(expr)

def convertChar2Int( expr):
    if (character.match(expr)):
        try:
            num = ord(expr)
            return str(num)
        except:
            print("ASCII value not found")
            sys.exit(1)
    return expr

def convertChar2Float( expr):
    expr = convertChar2Int(expr)
    return convertInt2Float(expr)

def convertChar2Short( expr):
    expr = convertChar2Int(expr)
    return convertInt2Short(expr)

def convertChar2Double( expr):
    return convertChar2Float(expr)

def convertChar2UInt( expr):
    expr = convertChar2Int(expr)
    return convertInt2UInt(expr)

def convertChar2Long( expr):
    return convertChar2Int(expr)

def convertChar2LongLong( expr):
    return convertChar2Int(expr)

def convertChar2ULong( expr):
    expr = convertChar2Int(expr)
    return convertChar2Long(expr)

def convertChar2UShort( expr):
    expr = convertChar2Int(expr)
    return convertInt2UShort(expr)

def convertChar2UChar( expr):
    expr = convertChar2Int(expr)
    return convertInt2UChar(expr)


def convertShort2Int( expr):
    num = int(expr)
    num &= 0xFFFFFFFF
    return str(num)

def convertShort2Char( expr):
    num = int(expr)
    num &= 0xFF
    return str(num)

def convertShort2Float( expr):
    num = int(expr)
    num &= 0xFFFFFFFF
    return str(num)+ '.00'

def convertShort2Double( expr):
    num = int(expr)
    return str(num) + '.00'

def convertShort2UInt( expr):
    return convertInt2UInt(expr)

def convertShort2Long( expr):        
    return convertInt2Long(expr)

def convertShort2LongLong( expr):
    return convertInt2LongLong(expr)

def convertShort2ULong( expr):
    return convertInt2ULong(expr)

def convertShort2UShort( expr):
    if ('-'.find(expr)):
        num = int(expr)
        num += 2 ** 16 
        num &= 0xFFFF
        return str(num)
    return expr

def convertShort2UChar( expr):
    if ('-'.find(expr)):
        num = int(expr)
        num += 2 ** 8
        num &= 0xFF
        return str(num)
    return str(int(expr) & 0xFF)


def convertDouble2Int( expr):
    num = int(float(expr))
    num &= 0xFFFFFFFF
    return str(num)
def convertDouble2Char( expr):
    expr = convertDouble2Int(expr)
    return convertInt2Char(expr)

def convertDouble2Short( expr):
    expr = convertDouble2Int(expr)    
    return convertInt2Short(expr)

def convertDouble2Float( expr):
    return expr

def convertDouble2UInt( expr):
    expr = convertDouble2Int(expr)
    return convertInt2UInt(expr)

def convertDouble2Long( expr):
    num = int(float(expr))
    num &= 0xFFFFFFFFFFFFFFFF
    return str(num)

def convertDouble2LongLong( expr):
    expr = convertDouble2Long(expr)
    return convertLong2LongLong(expr)

def convertDouble2ULong( expr):
    expr = convertDouble2Long(expr)
    return convertLong2ULong(expr)

def convertDouble2UShort( expr):
    expr = convertDouble2Short(expr)
    return convertShort2UShort(expr)

def convertDouble2UChar( expr):
    expr = convertDouble2Int(expr)
    return convertInt2Char(expr)

def convertUInt2Int( expr):
    if (num & 0x80000000) :
        num = (num & 0x7FFFFFFF) - (2 ** 32)
        return str(num)
    return str(num)

def convertUInt2Char( expr):
    expr = convertUInt2Int(expr)
    return convertInt2Char(expr)

def convertUInt2Short( expr):
    expr = convertUInt2Int(expr)
    return convertInt2Short(expr)

def convertUInt2Double( expr):
    expr = convertUInt2Int(expr)
    return convertInt2Double(expr)

def convertUInt2Float( expr):
    expr = convertUInt2Int(expr)
    return convertInt2Float(expr)

def convertUInt2Long( expr):
    expr = convertUInt2Int(expr)
    return convertInt2Long(expr)

def convertUInt2LongLong( expr):
    expr = convertUInt2LongLong(expr)
    return convertInt2LongLong(expr)

def convertUInt2ULong( expr):
    expr = convertUInt2Int(expr)
    return convertInt2ULong(expr)

def convertUInt2UShort( expr):
    expr = convertUInt2Int(expr)
    return convertInt2UShort(expr)

def convertUInt2UChar( expr):
    expr = convertUInt2Int(expr)
    return convertInt2UChar(expr)

def convertLong2Int( expr):
    return str(int(expr) & 0xFFFFFFFF)

def convertLong2Char( expr):
    return str(int(expr) & 0xFF)

def convertLong2Short( expr):
    return str(int(expr) & 0xFFFF)

def convertLong2Double( expr):
    expr = convertLong2Int(expr)
    return convertInt2Double(expr)

def convertLong2UInt( expr):
    expr = convertLong2Int(expr)
    return convertInt2UInt(expr)

def convertLong2Float( expr):
    expr = convertLong2Int(expr)
    return convertInt2Float(expr)

def convertLong2LongLong( expr):
    return str(int(expr) & 0xFFFFFFFFFFFFFFFF)

def convertLong2ULong( expr):
    if ('-'.find(expr)):
        num = int(expr)
        num += 2 ** 64
        num &= 0xFFFFFFFFFFFFFFFF
        return str(num)
    return str(num)

def convertLong2UShort( expr):
    expr = convertLong2Int(expr)
    return convertInt2UShort(expr)

def convertLong2UChar( expr):
    expr = convertLong2Int(expr)
    return convertInt2UChar(expr)

def convertLongLong2Int( expr):
    return str(int(expr) & 0xFFFFFFFF)

def convertLongLong2Char( expr):
    return str(int(expr) & 0xFF)

def convertLongLong2Short( expr):
    return str(int(expr) & 0xFFFF)

def convertLongLong2Double( expr):
    expr = convertLongLong2Int(expr)
    return convertInt2Double(expr)

def convertLongLong2UInt( expr):
    expr = convertLongLong2Int(expr)
    return convertInt2UInt(expr)

def convertLongLong2Long( expr):
    return expr

def convertLongLong2Float( expr):
    convertLongLong2Int(expr)
    return convertInt2Float(expr)

def convertLongLong2ULong( expr):
    return convertLong2ULong(expr)

def convertLongLong2UShort( expr):
    return convertLong2UShort(expr)
def convertLongLong2UChar( expr):
    return convertLong2UChar(expr)

def convertUShort2Int( expr):
    num = int(expr)
    if (num & 0x8000):
        num = (num & 0x7FFF) - (2 ** 16)
        return str(num & 0xFFFFFFFF)
    return str(num & 0xFFFFFFFF)

def convertUShort2Char( expr):
    expr = convertUShort2Int(expr)
    return convertInt2Char(expr)

def convertUShort2Short( expr):
    num = int(expr)
    if (num & 0x8000):
        num = (num & 0x7FFF) - (2 ** 16)
        return str(num & 0xFFFF)
    return str(num & 0xFFFF)

def convertUShort2Double( expr):
    expr = convertUShort2Int(expr)
    return convertInt2Double(expr)

def convertUShort2UInt( expr):
    return str(int(expr) &  0xFFFFFFFF)

def convertUShort2Long( expr):
    expr = convertUShort2Int(expr)
    return convertInt2Long(expr)

def convertUShort2LongLong( expr):
    expr = convertUShort2Int(expr)
    return convertInt2LongLong(expr)

def convertUShort2ULong( expr):
    expr = convertUShort2Int(expr)    
    return convertInt2ULong(expr)

def convertUShort2Float( expr):
    expr = convertUShort2Int(expr)
    return convertInt2Float(expr)

def convertUShort2UChar( expr):
    expr = convertUShort2Int(expr)
    return convertInt2UChar(expr)

def convertULong2Int( expr):
    expr = convertULong2Long(expr)
    return convertLong2Int(expr)

def convertULong2Char( expr):
    expr = convertULong2Long(expr)
    return convertLong2Char(expr)

def convertULong2Short( expr):
    expr = convertULong2Long(expr)
    return convertLong2Short(expr)

def convertULong2Double( expr):
    expr = convertULong2Long(expr)
    return convertLong2Double(expr)

def convertULong2UInt( expr):
    expr = convertULong2Long(expr)
    return convertLong2Int(expr)

def convertULong2Long( expr):
    num = int(expr)
    if (num & 0x8000000000000000):
        num = (num & 0x7FFFFFFFFFFFFFFF) - (2 ** 64)
        return str(num & 0xFFFFFFFFFFFFFFFF)
    return str(num & 0xFFFFFFFFFFFFFFFF)

def convertULong2LongLong( expr):
    return convertULong2Long(expr)

def convertULong2Float( expr):
    expr = convertULong2Long(expr)
    return convertLong2Float(expr)

def convertULong2UShort( expr):
    expr = convertULong2Long(expr)
    return convertLong2UShort(expr)

def convertULong2UChar( expr):
    expr = convertULong2Long(expr)
    return convertLong2UChar(expr)

def convertUChar2Int( expr):        
    if (character.match(expr)):
        try:
            num = ord(expr)
            return str(num)
        except: 
            print("ASCII value not found")
            sys.exit(1)
    else:
        return expr
def convertUChar2Char( expr):
    if (character.match(expr)):
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

def convertUChar2Short( expr):
    return convertUChar2Int(expr)

def convertUChar2Double( expr):
    expr = convertUChar2Int(expr)
    return convertInt2Double(expr)

def convertUChar2UInt( expr):
    if (character.match(expr)):
        try:
            num = ord(expr)
            return str(num)
        except:
            print("ASCII Value Not found")
            sys.exit(1)
    return expr

def convertUChar2Long( expr):
    return convertUChar2Int(expr)

def convertUChar2LongLong( expr):
    return convertUChar2Int(expr)

def convertUChar2ULong( expr):
    return convertUChar2UInt(expr)

def convertUChar2UShort( expr):
    return convertUChar2UInt(expr)

def convertUChar2Float( expr):
    return convertUChar2Double(expr)