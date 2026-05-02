# 🚀 K (Transpiler) --- Full Roadmap

## 🎯 Goal

Build a clean, modern language that transpiles to C++ using Python,
improving: - Syntax readability - Error messages - Developer experience

------------------------------------------------------------------------

## 🧱 Phase 0 --- Environment Setup

### Install tools

-   Python (3.10+)
-   C++ compiler (Clang recommended)
-   Basic editor (VS Code)

### Verify setup

-   Run Python scripts
-   Compile a simple C++ file using clang++

------------------------------------------------------------------------

## 🧠 Phase 1 --- Define Your Language (VERY IMPORTANT)

### Core Syntax Rules

#### Input / Output

    cout("hello world")
    cin(x)

#### Variables

    x:int = 5

#### Containers

    vector(int) = {}
    map(str,int)

#### Functions

    fn add(x:int, y:int) {
    }

#### Lambdas

    lambda[cpy]() {}
    lambda[ref]() {}

#### Pointers

    x:ptr(int)

#### Memory

    h = new int[10]
    delete h

#### Comments

    #{
    this is multiline
    }#

#### No semicolons

------------------------------------------------------------------------

## 🧩 Phase 2 --- Design the Compiler Pipeline

    Your Language → Lexer → Parser → AST → Transpiler → C++ → Clang → Executable

------------------------------------------------------------------------

## 🔍 Phase 3 --- Build a Lexer (Tokenizer)

Goal: Break input into tokens like: - keywords (fn, new, delete) -
identifiers (x, add) - symbols (:, =, {}, \[\])

Why: So your system understands structure, not just text.

------------------------------------------------------------------------

## 🌳 Phase 4 --- Build a Parser

Convert tokens into structured representation (AST)

Example:

    x:int = 5

Becomes:

    VariableDeclaration
      IDENT x
      colon :
      IDENT int
      symbol =
      value: 5
ex:
code = '''
x:int = 5
cout "hello"
h = new int[10]
'''

print(tokenize(code))

OUTPUT: 

[
 ('IDENT', 'x'),
 ('COLON', ':'),
 ('IDENT', 'int'),
 ('EQUAL', '='),
 ('NUMBER', 5),

 ('KEYWORD', 'cout'),
 ('STRING', '"hello"'),

 ('IDENT', 'h'),
 ('EQUAL', '='),
 ('KEYWORD', 'new'),
 ('IDENT', 'int'),
 ('LBRACKET', '['),
 ('NUMBER', 10),
 ('RBRACKET', ']')
]


------------------------------------------------------------------------

## 🌲 Phase 5 --- AST Design

Create node types: - VariableDeclaration - FunctionDeclaration -
FunctionCall - TypeNode - LambdaNode

------------------------------------------------------------------------

## 🔄 Phase 6 --- Transpiler (Core Engine)

Convert AST → C++

Examples:

### I/O

    cout "hi"
    → std::cout << "hi" << std::endl;

    x = cin
    → std::cin >> x;

### Types

    x:int = 5
    → int x = 5;

### Containers

    vector: int
    → std::vector<int>

### Functions

    fn add(x:int, y:int)
    → auto add(int x, int y)

### Lambdas

    ->[cpy]()
    → [=]()

    ->[ref]()
    → [&]()

### Memory

    h = new int[10]
    → int* h = new int[10];

    delete h
    → delete[] h;

------------------------------------------------------------------------

## ⚠️ Phase 7 --- Error System (IMPORTANT)

Your advantage over C++

### Add simple checks:

#### 1. Syntax Errors

-   Missing type after `:`
-   Invalid function declaration

#### 2. Type Errors

-   vector with wrong number of types
-   map missing key/value

#### 3. Helpful Messages

Instead of:

    error: expected ‘>’

Show:

    Error: map requires 2 types → map: key,value

#### 4. Line tracking

Always track line numbers for better debugging

------------------------------------------------------------------------

## 🧪 Phase 8 --- Testing

Create test files: - valid programs - invalid syntax - edge cases

------------------------------------------------------------------------

## 🛠️ Phase 9 --- CLI Tool

Make a command:

    mylang file.my

Steps: 1. Read file 2. Transpile 3. Save output.cpp 4. Call clang++ 5.
Run executable

------------------------------------------------------------------------

## 🔥 Phase 10 --- Improvements

-   Better parser (recursive descent)
-   Type checking
-   Modules/import system
-   Standard library mapping

------------------------------------------------------------------------

## 🧭 Final Advice

Start small: 1. Variables 2. cout / cin 3. Functions 4. Containers

Then grow step-by-step.

Avoid: - Regex-only parsing - Overcomplicating early

------------------------------------------------------------------------

## 🎉 Outcome

You will have: - A real programming language frontend - Cleaner syntax
than C++ - Better error messages - A solid compiler foundation
