from parsingComponents import *

class FunctionCall:
    def __init__(self, name:str, args:list):
        self.name = name
        self.args = args
    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"

def parseFunctionCall(token_line:list):
    name = token_line[0][1]
    if len(token_line) < 3 or token_line[1][0] != "LPAREN":
        raise SyntaxError(f"{name} must be followed by parentheses")
    i = 2
    args = []
    while i < len(token_line) and token_line[i][0] != "RPAREN":
        if token_line[i][0] != "COMMA":
            args.append(token_line[i])
        i += 1
    return FunctionCall(name, args)

def group_statements(tokens:list[list[tuple]]) -> list[list[tuple]]:
    
    '''
        Groups statements and assigns them depth as well (for proper nesting)
    '''
    STMT_KEYWORDS = {"cout", "cin", "fn", "lambda", "return", "if", "else", "elif", "delete", "break", "continue", "try", "except", "throw"}
    grouped = []
    current = []
    depth = 0
    for line in tokens:
        for tok in line:
            if not isinstance(tok, tuple):
                raise TypeError(f"Invalid token: {tok}, expected tuple")
            if tok[0] == "LBRACE":
                depth += 1
                current.append(tok)

            elif tok[0] == "RBRACE":
                depth -= 1
                current.append(tok)
                if depth == 0:
                    grouped.append(current)
                    current = []

            elif depth == 0 and current:
                if tok[0] == "IDENT" and current[-1][0] not in ("KEYWORD", "COLON", "EQUAL", "PLUS", "MINUS", "STAR", "SLASH", "MOD", "COMMA", "LPAREN", "LBRACKET", "EQEQ", "NEQ", "LT", "GT", "LEQ", "GEQ", "AND", "OR"):
                    grouped.append(current)
                    current = [tok]
                elif tok[0] == "KEYWORD" and tok[1] in STMT_KEYWORDS:
                    grouped.append(current)
                    current = [tok]
                else:
                    current.append(tok)
            else:
                current.append(tok)

        if current and depth == 0:
            grouped.append(current)
            current = []
    return grouped

def parser(tokens:list)->list:
    '''
        Creates an AST from all the tokens all together by parsing them one by one.
    
    '''
    # tokens = group_statements(tokens) 
    ## already doing before so that it is not called again while function parsing
    AST = []
    prev = None
    for token in tokens:
        stmt_type = statementType(token)
        if stmt_type == parseElse:
            if not isinstance(prev, IfStatement):
                raise SyntaxError("else without matching if")
        elif stmt_type == parseElif:
            if not isinstance(prev, IfStatement):
                raise SyntaxError("elif without matching if")
        node = stmt_type(token)
        AST.append(node)
        prev = node
    return AST
    
def statementType(token_line:list):
    
    '''
        A simple dispatcher to check what type of instruction there is and then assign a function to it
    '''
    
    if len(token_line) <=1:
        raise SyntaxError #TODO: decide what should the error message be
    if token_line[0][0] == "IDENT" and token_line[1][0] == "COLON":
        return parseVar
    elif token_line[0][0] == "IDENT" and token_line[1][0] == "EQUAL":
        return parseAssignment
    elif token_line[0][0] == "KEYWORD" and token_line[0][1] == "fn":
        return parseFunc
    elif token_line[0][0] == "KEYWORD" and token_line[0][1] == "lambda":
        return parseLambda
    elif token_line[0][0] == "KEYWORD" and token_line[0][1] == "return":
        return parseReturn
    elif token_line[0] == ("KEYWORD", "if"):
        return parseIf
    elif token_line[0] == ("KEYWORD", "else"):
        return parseElse
    elif token_line[0] == ("KEYWORD", "elif"):
        return parseElif
    elif token_line[0][0] == "KEYWORD" and token_line[0][1] in ("cout", "cin"):
        return parseFunctionCall
    else:
        raise SyntaxError(f"Could not find statement type: {token_line[0]}")


if __name__ == "__main__":
    def test():
        token = group_statements([[('KEYWORD', 'fn'), ('IDENT', 'main'), ('LPAREN', '('), ('RPAREN', ')'), ('LBRACE', '{'), ('KEYWORD', 'cout'), ('LPAREN', '('), ('STRING', "'hello world\n'"), ('RPAREN', ')'), ('IDENT', 'x'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 5), ('IDENT', 'y'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 4), ('IDENT', 'z'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 4), ('PLUS', '+'), ('NUMBER', 5), ('IDENT', 'x'), ('EQUAL', '='), ('NUMBER', 3), ('RBRACE', '}'), ('KEYWORD', 'fn'), ('IDENT', 'hello'), ('LPAREN', '('), ('IDENT', 'x'), ('COLON', ':'), ('IDENT', 'int'), ('RPAREN', ')'), ('LBRACE', '{'), ('KEYWORD', 'cout'), ('LPAREN', '('), ('STRING', '"This is a function\n"'), ('RPAREN', ')'), ('IDENT', 'x'), ('EQUAL', '='), ('NUMBER', 9), ('KEYWORD', 'return'), ('IDENT', 'x'), ('RBRACE', '}')]])
        print(token)
        obj = parser(token)
        print("========================================================")
        print(f"{obj}")
    test()
