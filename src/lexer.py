import re

TOKENS:list = [
    ("NUMBER",r"\d+"),
    ("STRING",r'"[^"]*"|\'[^\']*\''),
    ("ARROW",r"->"),
    ("MULTICOMMENT", r"///.*?///"),
    ("COMMENT", r"//.*"),
    ("COLON",r":"),
    ("COMMA",r","),
    ("EQUAL",r"="),
    ("STAR", r"\*"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("NEWLINE", r"\n"),
    ("SKIP",r"[ \t]+"),
    ("PLUS",r"\+"),
    ("MINUS",  r"\-"),
    ("SLASH",r"/"),
    ("MULT", r"\*"),
    ("MOD", r"\%"),
    ("AND", r"\&\&"),
    ("OR", r"\|\|"),
    ("NOT", r"\~"),
    ("MISMATCH", r"."),
]
KEYWORDS:set ={
    # my implemented keywords: (currently)
    "fn", "new", "delete", "cout", "cin",
    "vector", "map",
    "true", "false" ,
    "lambda", "return",
    "break", "continue",
    "try", "except", "throw", "if", "else", "elif"
    #TODO: slowly add more
}
TOKEN_RE= "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKENS)

def tokenise(lines:list[str]) -> list[list[tuple[str, str]]]: 
    '''
        Creates token by going through each line    
    '''
    
    tokens = []
    line_num = 1
    for line in lines:
        token = []
        for match in re.finditer(TOKEN_RE, line, re.DOTALL):
            kind = match.lastgroup
            value = match.group()
            if kind == "NUMBER":
                token.append(("NUMBER", int(value)))
            elif kind == "STRING":
                token.append(("STRING", value))
            elif kind == "IDENT":
                if value in KEYWORDS:
                    token.append(("KEYWORD", value))
                else:
                    token.append(("IDENT", value))
            elif kind == "NEWLINE":
                line_num += 1
            elif kind == "SKIP":
                continue
            elif kind == "MULTICOMMENT" or kind == "COMMENT":
                continue  # ignore comments
            elif kind == "MISMATCH":
                raise SyntaxError(f"Unexpected character: {value} at line {line_num}")
            
            else:
                token.append((kind,value))
        tokens.append(token)
    return tokens

###
if __name__ == "__main__":
    def test():
        code = ["""fn main(){
                cout('hello world\n')
                x: int = 5
                y:int = 4
                z:int = 4 + 5
                x = 3
                }
                """
                """fn hello(x:int){
                    cout("This is a function\n")
                    x = 9
                    return x
                }"""

                ]
        print(tokenise(code))
    test()
