import subprocess
import os


def checkFileExistance(file:str)->None:
    if not os.path.exists(file):
        raise FileNotFoundError
    pass

def read_file(input_file:str)->list[str]:
    
    '''
       Reads code file and converts it into a list of strings (one line per string)
    '''
    
    checkFileExistance(input_file)
    
    with open(input_file, 'r') as f:
        code = f.readlines()
    code = [x.strip().strip("\t") for x in code]
    
    return code

def write_file(input_file:str, cpp_code:list[str])->str:
    
    '''
        Creates the cpp file and writes the code to it
    '''
    
    output_file = f"./{input_file}.cpp"
    with open(output_file, 'w') as f:
        f.write("\n".join(cpp_code))
    return output_file

def compile_and_run(cpp_file:str)->None:
    """
    Does a 3 step process
    1. Compiles the C++ file.
    2. Runs the executable file
    3. Deletes the executable and C++ file
    """ 
    
    checkFileExistance(cpp_file)
    
    exe_file = f"{cpp_file[:-4]}" # Hence same name as the cpp file
    try:
        compile_cmd = ["clang++", cpp_file, "-o", exe_file]
        print("Compiling...")
        subprocess.run(compile_cmd, check=True)

        print("Running executable...\n")
        subprocess.run(["./" + exe_file], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    finally:
        # if os.path.exists(exe_file):
        #     os.remove(exe_file)
        #allowing users to actually keep the executable to avoid re-compiling each time
        if os.path.exists(cpp_file):
            os.remove(cpp_file)
