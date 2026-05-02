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
        from parser import parser
        return ReturnStatement(parser([value])[0])

class FunctionDeclaration:
    def __init__(self, name:str, params:list, content:list):
        self.name = name
        self.params = self.param_parser(params)
        self.content = self.content_parser(content)
    def content_parser(self, content):
        
        from parser import parser #imported hear to avoid circular imports
        
        i = -1
        if ("KEYWORD", "return") in content:
            ret_index = content.index(("KEYWORD", "return"))
            main_content = content[:ret_index]
        else:
            main_content = content
            
        return parser([main_content])
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
    while token_line[i][0] != "RPAREN":
        try:
            params.append(token_line[i])
            i+=1
        except IndexError:
            raise IndexError("Parenthesis is not closed in function declaration")
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