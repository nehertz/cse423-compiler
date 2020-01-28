import re
from TokenName import TokenName
import sys

"""
Creates a dictionary with fixed-value tokens as the key
and their token definition as the value
"""
def create_token_defs():
    tokens_dict = {}

    # Create dict entries for type specifiers
    tokens_dict['auto'] = TokenName.TypeSpecifier
    tokens_dict['union'] = TokenName.TypeSpecifier
    tokens_dict['short'] = TokenName.TypeSpecifier
    tokens_dict['double'] = TokenName.TypeSpecifier
    tokens_dict['long'] = TokenName.TypeSpecifier
    tokens_dict['unsigned'] = TokenName.TypeSpecifier
    tokens_dict['int'] = TokenName.TypeSpecifier
    tokens_dict['char'] = TokenName.TypeSpecifier
    tokens_dict['static'] = TokenName.TypeSpecifier
    tokens_dict['volatile'] = TokenName.TypeSpecifier
    tokens_dict['struct'] = TokenName.TypeSpecifier
    tokens_dict['extern'] = TokenName.TypeSpecifier
    tokens_dict['signed'] = TokenName.TypeSpecifier
    tokens_dict['const'] = TokenName.TypeSpecifier
    tokens_dict['enum'] = TokenName.TypeSpecifier
    tokens_dict['void'] = TokenName.TypeSpecifier
    tokens_dict['float'] = TokenName.TypeSpecifier

    # Create dict entries for keywords
    tokens_dict['else'] = TokenName.Keyword
    tokens_dict['register'] = TokenName.Keyword
    tokens_dict['do'] = TokenName.Keyword
    tokens_dict['goto'] = TokenName.Keyword
    tokens_dict['continue'] = TokenName.Keyword
    tokens_dict['if'] = TokenName.Keyword
    tokens_dict['sizeof'] = TokenName.Keyword
    tokens_dict['switch'] = TokenName.Keyword
    tokens_dict['for'] = TokenName.Keyword
    tokens_dict['case'] = TokenName.Keyword
    tokens_dict['while'] = TokenName.Keyword
    tokens_dict['break'] = TokenName.Keyword
    tokens_dict['return'] = TokenName.Keyword
    tokens_dict['default'] = TokenName.Keyword

    # Create dict entries for operators
    # Arithmetic
    tokens_dict['+'] = TokenName.ArithmeticOperator
    tokens_dict['-'] = TokenName.ArithmeticOperator
    tokens_dict['*'] = TokenName.ArithmeticOperator
    tokens_dict['/'] = TokenName.ArithmeticOperator
    tokens_dict['%'] = TokenName.ArithmeticOperator
    # Increment
    tokens_dict['++'] = TokenName.Increment
    # Decrement
    tokens_dict['--'] = TokenName.Decrement
    # Comparison
    tokens_dict['=='] = TokenName.ComparisonOperator
    tokens_dict['!='] = TokenName.ComparisonOperator
    tokens_dict['>'] = TokenName.ComparisonOperator
    tokens_dict['<'] = TokenName.ComparisonOperator
    tokens_dict['>='] = TokenName.ComparisonOperator
    tokens_dict['<='] = TokenName.ComparisonOperator
    # Logical
    tokens_dict['&&'] = TokenName.LogicalOperator
    tokens_dict['||'] = TokenName.LogicalOperator
    tokens_dict['!'] = TokenName.LogicalOperator
    # Assignment
    tokens_dict['='] = TokenName.AssignmentOperator
    tokens_dict['+='] = TokenName.AssignmentOperator
    tokens_dict['-='] = TokenName.AssignmentOperator
    tokens_dict['*='] = TokenName.AssignmentOperator
    tokens_dict['/='] = TokenName.AssignmentOperator
    tokens_dict['%='] = TokenName.AssignmentOperator
    tokens_dict['<<='] = TokenName.AssignmentOperator
    tokens_dict['>>='] = TokenName.AssignmentOperator
    tokens_dict['&='] = TokenName.AssignmentOperator
    tokens_dict['^='] = TokenName.AssignmentOperator
    tokens_dict['|='] = TokenName.AssignmentOperator
    # SpecialCharacter

    # BitwiseOperator
    tokens_dict['>>'] = TokenName.BitwiseOperator
    tokens_dict['<<'] = TokenName.BitwiseOperator
    tokens_dict['~'] = TokenName.BitwiseOperator
    tokens_dict['&'] = TokenName.BitwiseOperator
    tokens_dict['^'] = TokenName.BitwiseOperator
    tokens_dict['|'] = TokenName.BitwiseOperator
    # LParen
    tokens_dict['('] = TokenName.LParen
    # RParaen
    tokens_dict[')'] = TokenName.RParen
    # LBracket
    tokens_dict['{'] = TokenName.LBracket
    # RBracket
    tokens_dict['}'] = TokenName.RParen
    # LCurly
    tokens_dict['['] = TokenName.LCurly
    # RCurly
    tokens_dict[']'] = TokenName.RCurly
    # LAngle
    tokens_dict['<'] = TokenName.LAngle
    # RAngle
    tokens_dict['>'] = TokenName.RAngle
    # Semicolon
    tokens_dict[';'] = TokenName.Semicolon
    # Colon
    tokens_dict[':'] = TokenName.Colon
    # Comma
    tokens_dict[','] = TokenName.Comma
    # Single quote
    tokens_dict['\''] = TokenName.SingleQuot
    # Souble quote
    tokens_dict['\"'] = TokenName.DoubleQuot

    # TODO: Add rest of fixed-value tokens

    return tokens_dict


"""
Takes in a token and assigns it a token definition
"""
def tokenize(tokens):

    re_word = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*$")
    tokens_dict = create_token_defs()
    re_string = re.compile("((\")|(\'))[\w\d]((\")|(\'))")
    re_numconst = re.compile(r"(^\d*\.?\d*$)")
    for token in tokens:
        if (token in tokens_dict): 
            n = tokens_dict[token]
            print("< " + token + " , " + TokenName(n).name + " >")
        elif (re_numconst.match(token)):
            print("< " + token + " , " + "NumConst >")
        elif (re_word.match(token)):
            print("< " + token + " , " + "Identifier >")
        elif (re_string.match(token)):
            print("< " + token + " , " + "String >")
        else:
            pass
    """
    TODO: Check if token is directly indexable in the dict
    If not, check for strings, identifiers, numbers, and anything else
    that doesn't have a fixed value
    """


"""
Scans through a file and splits it into tokens
"""
def scan(fileString):
    # Regex to find valid C word
    re_id_first = re.compile(r"[a-zA-Z_]")
    re_id_after = re.compile(r"[a-zA-Z0-9_]")
    # Regex to find special character
    re_spec = re.compile(r"[^a-zA-Z0-9\s]")
    re_spec_2nd_char = "+-><=|&/*" 
    re_spec_3rd_char = "="
    # re_whtspace = re.compile("[\s]")

    three_char_ops = [['<', '<', "="], ['>', '>', '=']]
    two_char_ops = [['=', '='], ['!', '='], ['>', '='], ['<', '='], ['&', '&'], ['|', '|'], ['+', '='], ['-', '='],
                    ['*', '='], ['/', '='], ['%', '='], ['&', '='], ['^', '='], ['|', '='], ['+', '+'], ['-', '-'], ['<', '<'], ['>', '>']]
    one_char_ops = ['+', '-', '*', '/', '%', '=', '~', '&', '^', '|',
                    ',', ';', '"', '\'', '(', ')', '{', '}', '[', ']', '<', '>', ':', '?', '!']
    # token_dict = {}
    tokens = []
    comments = []
    lineNum = 1
    curr_token = ''
    index = 0
    # file_len = len(fileString)
    fileIndexReached = False
    fileString = fileString + ' '
    # print(fileString)
    while (not fileIndexReached):
        if (index >= len(fileString)):
            fileIndexReached = True
            break

        
        try:
            """ Checking for words, numbers, special characters, comments, and strings """
            c = fileString[index]
            
            if (re.search(r"\s", c)):
                # The character is a white space character
                if (c == '\n'):
                    # New line char found, increment line num
                    lineNum += 1
                    index += 1
                    
                    curr_token = ''
                    continue
                else:
                    # Skip white space character
                    if (curr_token != ""):
                        tokens.append(curr_token)
                        index += 1
                        curr_token = ''
                        continue
                    

            if (re.search(re_id_first, c) != None):
                # The character is a character of an id/keyword
                curr_token += c

                while (re.search(re_id_after, fileString[index + 1]) != None):
                    # Continue looking for valid id/keyword characters
                    index += 1
                    curr_token += fileString[index]

                # All valid characters found, append full token to token list
                tokens.append(curr_token)
                index += 1
                curr_token = ''
                continue

            elif (c.isnumeric()):
                # The character is a number
                curr_token += c

                while (fileString[index + 1].isnumeric() or fileString[index + 1] == '.'):
                    # Keep checking for more digits or decimal point in the number
                    index += 1
                    curr_token += fileString[index]

                # All digits found, append full token to token list
                tokens.append(curr_token)
                curr_token = ''
                index += 1
                continue

            elif(re.search(re_spec, c) != None):
                # The character is a special character
                curr_token += c
                
                index += 1

                # if (re.search(re_spec_2nd_char, fileString[index]) != None):
                if (fileString[index] in re_spec_2nd_char):

                    curr_token += fileString[index]
                    index += 1
                    if (fileString[index] in re_spec_3rd_char):
                        # Check for three-character operator
                        curr_token += fileString[index]
                        index += 1
                        i = 0
                        while True:
                            # Going through the loop on three_char_ops
                            # and finding which operator matches the current token
                            # if matched then break and work with the corresponding
                            # i. Else continue
                            try:
                                if (curr_token == ''.join(three_char_ops[i])):

                                    break
                            except StopIteration:
                                print("In special char, three_char_spec Not found ")
                                break
                            except:
                                print("Error occurred three_char_ops")
                                print(sys.exc_info()[0])
                                break
                            i += 1

                        # We need a mapping of operators to Name.
                        continue
                    else:
                    # two character operator
                    # curr_token += fileString[index]
                    # index += 1
                        if (curr_token == '//'):
                            # Single line comments
                            # while (fileString[index] not "\n"):
                            while ("\n" != fileString[index]):
                                curr_token += fileString[index]
                                index += 1
                            comments.append(curr_token)
                            curr_token = ''
                            index += 1
                            continue

                        elif (curr_token == '/*'):
                            # Multi-line comments
                            end_tracker = fileString[index]
                            while True:
                                if (end_tracker == '*'):
                                    curr_token += fileString[index]
                                    index += 1
                                    if (fileString[index] == '/'):
                                        # Comment ended successfully
                                        
                                        curr_token += fileString[index]
                                        index += 1
                                        break
                                else:
                                    if (fileString[index] == ''):
                                        # EOF reached
                                        break

                                    if (fileString[index] == '\n'):
                                        lineNum += 1
                                    curr_token += fileString[index]
                                    index += 1
                                    end_tracker = fileString[index]
                            ## index += 1
                            comments.append(curr_token)
                            curr_token = ''
                            continue
                        else:
                            pass
                        i = 0

                        while True:
                            # Going thru the loop on two_char_ops
                            # and finding which operator matches the current_token
                            # if matched then break and work with the corresponding i
                            # else continue
                            # if i goes beyond the size of two_char_ops printout error message
                            try:
                                if (curr_token == ''.join(two_char_ops[i])):
                                    tokens.append(curr_token)
                                    curr_token = ''
                                    index += 1
                                    break
                            except IndexError:
                                print("In Special Char, Two_char_spec Not found")
                                print(curr_token)
                                break
                            except:
                                print("error occurred two_char_spec")
                                print(sys.exc_info()[0])
                                break
                            i += 1

                        # We need a mapping of operators to their name
                        continue
                else:
                    
                    # one character operator

                    # Check for quotation first
                    if (curr_token == '"'):
                        while (fileString[index] != '"'):
                            # We do not yet take care of Escape character strings
                            curr_token += fileString[index]
                            index += 1

                        # Send strings to the tokenizer
                        tokens.append(curr_token)
                        index += 1
                        curr_token = ''
                        continue

                    elif (curr_token == "'"):
                        while (fileString[index] != "'"):
                            # We do not yet take care of Escape character strings
                            curr_token += fileString[index]
                            index += 1
                        tokens.append(curr_token)
                        index += 1
                        curr_token = ''
                        continue
                    else:
                        pass

                    i = 0
                    listSizeReached = False
                    while (not listSizeReached):
                        # Going thru the loop on one_char_ops
                        # and finding which operator matches the current_token
                        # if matched then break and work with the corresponding i
                        # else continue
                        # if i goes beyond the size of one_char_ops printout an error msg
                        # # i = 0
                        try:
                            if (curr_token == one_char_ops[i]):
                                tokens.append(curr_token)
                                curr_token = ''
                                i += 1
                                break
                        except IndexError:
                            print("In special char, one_char_ops Not found")
                            print(sys.exc_info()[0])
                            print(curr_token)
                            listSizeReached = True
                            break
                        except:
                            print("error occurred one_char_ops")
                            break
                        i += 1
                    continue
            index += 1
        except IndexError:
            fileIndexReached = True

    print (comments)
    return tokens
