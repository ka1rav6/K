from .VariableParser import parseVar

class ReturnStatement:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"return {self.value}"

def parseReturn(token_line:list):
        if len(token_line) < 2:
            raise SyntaxError("return must have a value")
        value = token_line[1:]
        if len(value) == 1:
            return ReturnStatement(value[0])
        # Only re-parse if value looks like a statement (var decl, assignment, etc.)
        # Otherwise treat as a raw expression (e.g. a + b, x * 2)
        first = value[0]
        is_statement = (
            (first[0] == "KEYWORD") or
            (len(value) >= 2 and first[0] == "IDENT" and value[1][0] in ("COLON", "EQUAL"))
        )
        if is_statement:
            from parser import parser, group_statements
            grouped = group_statements([value])
            return ReturnStatement(parser(grouped)[0])
        # Raw expression — store token list directly
        return ReturnStatement(value)

class FunctionDeclaration:
    def __init__(self, name:str, params:list, content:list):
        self.name = name
        self.params = self.param_parser(params)
        self.content = self.content_parser(content)
    def content_parser(self, content):
        
        from parser import parser, group_statements
        
        grouped = group_statements([content])
        return parser(grouped)
    def param_parser(self, params:list)->list:
        parsed = []
        current = []
        for token in params:
            if token[0] == "COMMA":
                if current:
                    parsed.append(parseVar(current))
                    current = []
            else:
                current.append(token)
        if current:
            parsed.append(parseVar(current))
        return parsed
   
def parseFunc(token_line:list)->FunctionDeclaration:
    if len(token_line)< 5:
        raise SyntaxError("Function Declaration should have the syntax: fn name(){}")
    i = 0
    if token_line[i][0] != "KEYWORD" or token_line[i][1] != "fn":
        raise SyntaxError("Function Declaration should have the syntax: fn name(){}")
    i += 1
    name = token_line[i][1] if token_line[i][0] == "IDENT" else None
    if not name:
        raise SyntaxError("function should have a name")
    i+=1
    if token_line[i][0] != "LPAREN":
        raise SyntaxError("function declaration should be followed by parenthesis")
    i+=1
    params = []
    while i < len(token_line) and token_line[i][0] != "RPAREN":
        params.append(token_line[i])
        i+=1
    if i >= len(token_line):
        raise SyntaxError("Parenthesis is not closed in function declaration")
    i+=1
    if token_line[i][0] != "LBRACE":
        raise SyntaxError("Functions should be followed by curly braces inside which the function is defined")
    i += 1
    content = []
    depth = 1
    while depth > 0:
        try:
            tok = token_line[i]
            if tok[0] == "LBRACE":
                depth += 1
            elif tok[0] == "RBRACE":
                depth -= 1
                if depth == 0:
                    break
            content.append(tok)
            i += 1
        except IndexError:
            raise IndexError("Function content curly braces are never closed")
    i+=1
    return FunctionDeclaration(name, params, content)




def parseLambda(token_line:list)->FunctionDeclaration: #type:ignore
    pass