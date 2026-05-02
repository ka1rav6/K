import sys
from lexer import tokenise
from ASTtoCpp import to_cpp
from fileio import read_file, write_file, compile_and_run

FILE = sys.argv[1]

if __name__ == "__main__":
    
    code:list[str] = read_file(FILE)
    tokens:list = tokenise(code)
    
    cpp_code = []
    for token in tokens:
        cpp_code.append(to_cpp(token))
    cpp_file = write_file(cpp_code)
    compile_and_run(cpp_file)
