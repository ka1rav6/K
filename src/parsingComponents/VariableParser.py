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
        if token_line[i][0] == "EQUAL":
            i+=1
            value = token_line[i][1]
            i+=1            
    
    return VariableDeclaration(name, type, value)

def parseAssignment(token_line:list)->VariableDeclaration: #type:ignore
    pass
