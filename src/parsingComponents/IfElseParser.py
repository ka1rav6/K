
#### How i want the format:
#if x == 3{
#     x = x + 4    
# }

class IfStatement:
    def __init__(self, condition: list, content:list):
        self.condition = condition
        self.content = self.parsecontent(content)
    def parsecontent(self, content:list):
        from parser import parser, group_statements
        grouped = group_statements([content])
        return parser(grouped)
class ElseStatement:
    def __init__(self, content:list):
        self.content = self.parsecontent(content)
    def parsecontent(self, content:list):
        from parser import parser, group_statements
        grouped = group_statements([content])
        return parser(grouped)
def parseIf(token_line:list):
    i = 1
    condition = []

    while token_line[i][0] != "LBRACE":
        condition.append(token_line[i])
        i += 1
    i += 1 
    content = []
    depth = 1
    while depth > 0:
        tok = token_line[i]
        if tok[0] == "LBRACE":
            depth += 1
        elif tok[0] == "RBRACE":
            depth -= 1
            if depth == 0:
                break
        content.append(tok)
        i += 1

    return IfStatement(condition, content)

def parseElse(token_line:list):
    if token_line[1][0] != "LBRACE":
        raise SyntaxError("else must be followed by a block")
    i = 2
    content = []
    depth = 1
    while depth > 0:
        tok = token_line[i]
        if tok[0] == "LBRACE":
            depth += 1
        elif tok[0] == "RBRACE":
            depth -= 1
            if depth == 0:
                break
        content.append(tok)
        i += 1

    return ElseStatement(content)

def parseElif(token_line:list):
    i = 1
    condition = []

    while token_line[i][0] != "LBRACE":
        condition.append(token_line[i])
        i += 1

    i += 1

    content = []
    depth = 1
    while depth > 0:
        tok = token_line[i]
        if tok[0] == "LBRACE":
            depth += 1
        elif tok[0] == "RBRACE":
            depth -= 1
            if depth == 0:
                break
        content.append(tok)
        i += 1

    return IfStatement(condition, content)  # reuse same class