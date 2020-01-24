import re

def scan(fileString):
    keywords = ['auto', 'else', 'register', 'union', 'do', 'goto', 'short', 'double',
                'long', 'typedef', 'continue', 'if', 'sizeof', 'unsigned', 'int', 'switch', 'char',
                'for', 'static', 'volatile', 'struct', 'case', 'extern', 'signed', 'while', 'const',
                'break', 'enum', 'return', 'void', 'default', 'float']
                
    # Regex to find valid C word
    re_id_first = re.compile(r"[a-zA-Z_]")
    re_id_after = re.compile(r"[a-zA-Z0-9_]")
    # Regex to find special character
    re_spec = re.compile(r"[^a-zA-Z0-9\s]")
    # Regex to find semicolon
    re_semi = re.compile("[;]")
    # Regexes to find parens
    re_lparen = re.compile("[(]")
    re_rparen = re.compile("[)]")
    # Regexes to find brackets
    re_lbrack = re.compile("[[]")
    re_rbrack = re.compile("[]]")
    # Regexes to find curly brackets
    re_lcurly = re.compile("[{]")
    re_rcurly = re.compile("[}]")
    # Regexes to find angle brackets
    re_langle = re.compile("[<]")
    re_rangle = re.compile("[>]")
    # Regexes to find arithmetic operators
    re_arith = re.compile("[\+\-\*\/\%]")

    three_char_ops = [['<', '<', "="], ['>', '>', '=']]
    two_char_ops = [['=', '='], ['!', '='], ['>', '='], ['>', '='], ['&', '&'], ['|', '|'], ['+', '='], ['-', '='], ['*', '='], ['/', '='], ['%', '='], ['&', '='], ['^', '='], ['|', '='], ['+', '+'], ['-', '-'], ['<', '<'], ['>', '>']]

    tokens = []
    comments = []    
    lineNum = 1
    curr_token = ''
    index = 0
    file_len = len(fileString)
    while True:
        """ Checking for words, numbers, special characters, comments, and strings """
        c = fileString[index]
        
        if (re.search(r"\s", c)):
            # The character is a white space character
            if (c == '\n'):
                # New line char found, increment line num
                lineNum += 1
                index += 1
                continue
            else:
                # Skip white space character
                index += 1
                continue

        if (re.search(re_id_first, c) != None):
            # The character is a character of an id/keyword
            curr_token += c
            
            while (re.search(re_id_after, fileString[index + 1]) != None):
                index += 1
                curr_token += fileString[index]
            
            # All letters found, append full token to token list
            tokens.append(curr_token)
            index += 1
            curr_token = ''
            continue
        
        elif (c.isnumeric()):
            # The character is a number
            curr_token += c
            
            while (fileString[index].isnumeric() or fileString[index] == '.'):
                # Keep checking for more digits or decimal point in the number
                index += 1
                curr_token += fileString[index]

            # All digits found, append full token to token list
            tokens.append(curr_token)
            index += 1
            curr_token = ''
            continue

        elif(re.search(re_spec, c) != None):
            # The character is a special character

            curr_token += c
            index += 1
            
            if (re.search(re_spec, fileString[index] != None):
                curr_token += fileString[index]
                index += 1
                if (re.search(re_spec, fileString[index]) != None):
                    # three character operator
                    
                else:
                    
                    # two character operator 
                    
            else:
                # one character operator
            
        elif(c == "/")
            if fileString[index + 1] == "/":
                while (fileString[index] != "\n"):
                    index += 1
                    curr_token += fileString[index]
                comments.append(curr_token)

            elif fileString[index + 1].isnumeric():
                index += 1
                
            elif fileString[index + 1] == "*":
                while (fileString[index] != "*" and fileString[index + 1] != "/"):
                    index += 1
                    curr_token += fileString[index]
                    
                    
                comments.append(curr_token)    
            index += 1
            curr_token = ''
            continue

             
            
        
        
            # Check if character is / (comment)
            
            # Check if character is three-char op

            index = index + 1