import sys
from lexer import tokenise
from parser import parser, group_statements
from ASTtoCpp import to_cpp
from fileio import read_file, write_file, compile_and_run

FILE = sys.argv[1]

if __name__ == "__main__":
    
    code:list[str] = read_file(FILE)
    tokens:list = tokenise(code)
    tokens = group_statements(tokens)
    AST = parser(tokens)
    
    cpp_code = to_cpp(AST)
    if cpp_code is None:
        print("AST generated successfully:")
        for node in AST:
            print(f"  {node}")
        print("\nTranspiler (ASTtoCpp) not yet implemented. Skipping compilation.")
    else:
        cpp_file = write_file(FILE, cpp_code)
        compile_and_run(cpp_file)
