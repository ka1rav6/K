from parsingComponents.VariableParser import parseVar, parseAssignment
from parsingComponents.FunctionParser import parseFunc, parseLambda, parseReturn
from parsingComponents.IfElseParser import parseIf, parseElse, IfStatement, parseElif

def group_statements(tokens:list[list[tuple]]) -> list[list[tuple]]:
    
    '''
        Groups statements and assigns them depth as well (for proper nesting)
    '''
    grouped = []
    current = []
    depth = 0
    for line in tokens:
        for tok in line:
            if tok[0] == "LBRACE":
                depth += 1
                current.append(tok)

            elif tok[0] == "RBRACE":
                depth -= 1
                current.append(tok)
                if depth == 0:
                    grouped.append(current)
                    current = []

            elif tok[0] == "KEYWORD" and tok[1] == "return" and depth == 0:
                if current:
                    grouped.append(current)
                current = [tok]
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
    tokens = group_statements(tokens)
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
    else:
        raise SyntaxError("Could not find statement type")


if __name__ == "__main__":
    def test():
        token = [('KEYWORD', 'fn'), ('IDENT', 'main'), ('LPAREN', '('), ('RPAREN', ')'), ('LBRACE', '{'), ('KEYWORD', 'cout'), ('LPAREN', '('), ('STRING', "'hello world\n'"), ('RPAREN', ')'), ('IDENT', 'x'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 5), ('IDENT', 'y'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 4), ('IDENT', 'z'), ('COLON', ':'), ('IDENT', 'int'), ('EQUAL', '='), ('NUMBER', 4), ('PLUS', '+'), ('NUMBER', 5), ('IDENT', 'x'), ('EQUAL', '='), ('NUMBER', 3), ('RBRACE', '}'), ('KEYWORD', 'fn'), ('IDENT', 'hello'), ('LPAREN', '('), ('IDENT', 'x'), ('COLON', ':'), ('IDENT', 'int'), ('RPAREN', ')'), ('LBRACE', '{'), ('KEYWORD', 'cout'), ('LPAREN', '('), ('STRING', '"This is a function\n"'), ('RPAREN', ')'), ('IDENT', 'x'), ('EQUAL', '='), ('NUMBER', 9), ('KEYWORD', 'return'), ('IDENT', 'x'), ('RBRACE', '}')] 

        obj = parseFunc(token)
        
        print(f"{obj.name} , {obj.params}, {obj.content} ")
    test()
