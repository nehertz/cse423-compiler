import ply.yacc as yacc


# Grammar rule functions, should be modified to follow the AST Construction. 
# Refer to section 6.10, PLY-documentation. NEED TO DECIDE WHICH APPOARCH WE WANT TO DO



# Build the parser and pass lex into the parser
def parser(lex):
    parser = yacc.yacc()
    parser.parse(lexer=lex)