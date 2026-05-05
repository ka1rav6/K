
def untokenise(token:list[tuple[str,str]])->str:
    line = " ".join([str(i[1]) for i in token]) #TODO: Fix this to show only one line
    return line
if __name__ == "__main__":
    def test():
        token = [('KEYWORD', 'fn'), ('IDENT', 'main'), ('LPAREN', '('), ('RPAREN', ')'), ('LBRACE', '{'), ('KEYWORD', 'cout'), ('LPAREN', '('), ('STRING', "'hello world\n'"), ('RPAREN', ')'), ('IDENT', 'x'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 5), ('IDENT', 'y'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 4), ('IDENT', 'z'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 4), ('PLUS', '+'), ('NUMBER', 5), ('IDENT', 'x'), ('EQUAL', '='), ('NUMBER', 3), ('RBRACE', '}'), ('KEYWORD', 'fn'), ('IDENT', 'hello'), ('LPAREN', '('), ('IDENT', 'x'), ('COLON', ':'), ('IDENT', 'int'), ('RPAREN', ')'), ('LBRACE', '{'), ('KEYWORD', 'cout'), ('LPAREN', '('), ('STRING', '"This is a function\n"'), ('RPAREN', ')'), ('IDENT', 'x'), ('EQUAL', '='), ('NUMBER', 9), ('KEYWORD', 'return'), ('IDENT', 'x'), ('RBRACE', '}')] 
        print(untokenise(token))
    test()
