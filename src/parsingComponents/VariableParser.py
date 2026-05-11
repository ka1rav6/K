class PtrType:
    def __init__(self, base:str = "int"):
        self.base = base
class Deref:
    def __init__(self, baseVar):
        self.baseVar = baseVar
        
        
class VariableDeclaration:
    def __init__(self, name:str, type:object, value = None):
        self.name:str = name
        self.type:object = type
        self.value = value
    def __repr__(self):
        return f"""
    name = {self.name}
    type = {self.type}                    
    value = {self.value}                    
    """

def parseVar(token_line:list)->VariableDeclaration:
    if len(token_line) <3:
            raise SyntaxError(f"Variable declaration syntax= name:type = VALUE or name:type")
    i = 0 #views tokens one by one
    name = token_line[i][1] if token_line[i][0] == "IDENT" else None
    if not name:
        raise SyntaxError("Variable declaration must have a name")
    i +=1
    if  token_line[i][0] != "COLON":
        raise SyntaxError(f"Variable declaration syntax: name:type = VALUE")
    i +=1
    type = token_line[i][1] if token_line[i][0] == "IDENT" else None
    if not type:
        raise SyntaxError("Variable declaration must have a type")
    i +=1
    if type == "ptr":
        if len(token_line) < 6:
            raise SyntaxError(f"Variable {name} of type ptr should have the syntax: {name}:ptr(type) = VALUE")
        
        if token_line[i][0] != "LPAREN":
            raise SyntaxError(f"Variable {name} of type ptr should have the syntax: {name}:ptr(type) = VALUE")
        i +=1 
        type = PtrType(base = token_line[i][1])
        i+=1
        if token_line[i][0] != "RPAREN":
            raise SyntaxError(f"Variable {name} of type ptr should have the syntax: {name}:ptr(type) = VALUE")
        i+=1
        if token_line[i][0] != "EQUAL":
            if len(token_line) != i+1:
                raise SyntaxError(f"Variable {name} of type ptr should have the syntax: {name}:ptr(type) = VALUE")
            else:
                return VariableDeclaration(name, type)
        i+=1
        if token_line[i][0] == "STAR":
            value = Deref(baseVar = token_line[i+1][1])
            i+=2
        else:
            value = token_line[i][1]
            i+=1       
        return VariableDeclaration(name, type, value)

    elif len(token_line) == i:
            return VariableDeclaration(name, type)
    else:
        #TODO: vector, map etc cases
        value = None
        if token_line[i][0] == "EQUAL":
            i+=1
            remaining = token_line[i:]
            if len(remaining) == 1:
                value = remaining[0][1]
            else:
                # Multi-token expression (e.g. 4 + 5) — store as token list
                value = remaining
    
    return VariableDeclaration(name, type, value)

class Assignment:
    def __init__(self, name:str, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Assignment({self.name} = {self.value})"

def parseAssignment(token_line:list):
    if len(token_line) < 3:
        raise SyntaxError("Assignment syntax: name = VALUE")
    name = token_line[0][1]
    if token_line[1][0] != "EQUAL":
        raise SyntaxError("Assignment syntax: name = VALUE")
    # Collect value tokens — could be a single value or an expression
    value_tokens = token_line[2:]
    if len(value_tokens) == 1:
        value = value_tokens[0][1]
    else:
        # For expressions like 4 + 5, store as a list of tokens
        value = value_tokens
    return Assignment(name, value)
