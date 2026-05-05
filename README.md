# K Language (C++-Backed Custom Language)

## Overview

**K** is a custom programming language designed as a cleaner, more readable alternative to C++, while still leveraging C++'s performance and memory model.

Instead of modifying existing compilers, K is implemented as a **transpiler**:

* K source code → converted to C++
* C++ → compiled using a standard compiler (e.g., Clang)

This allows K to remain lightweight while still producing efficient native binaries.

---

## Goals

* Simplify C++ syntax
* Improve readability
* Provide better error messages
* Retain low-level control (pointers, manual memory management)
* Build a structured compiler pipeline from scratch

---

## Syntax Design

### Input / Output

```k
cout("hello world")
cin(x)
```

---

### Variables

```k
x:int = 5
x:int
```

---

### Pointers

```k
x:ptr(int)
x:ptr(int) = y
x:ptr(int) = *y
```

---

### Memory Management

```k
h = new int[10]
delete h
```

---

### Functions

```k
fn add(x:int, y:int) {
}
```

---

### Lambdas

```k
lambda[cpy]() {}
lambda[ref]() {}
```

---

### Containers

```k
vector(int) = {}
map(str, int)
```

---

### Comments

```k
#{
this is a multiline comment
#}
```

---

### No Semicolons

Statements are separated by structure, not `;`.

---

## Architecture

The project follows a standard compiler front-end pipeline:

```
K Source Code
    ↓
Lexer (tokenization)
    ↓
Parser (AST generation)
    ↓
Transpiler (C++ generation)
    ↓
Clang / g++
    ↓
Executable
```

---

## Current Status

### Implemented

* Token-based parsing structure
* Statement detection system
* Variable declaration parsing
* Pointer type parsing (`ptr(int)`)
* Basic dereference handling (`*x`)

---

### In Progress

* Expression parsing
* Function parsing
* Lambda parsing
* Type system expansion (vector, map)
* Error reporting improvements
* AST node structure (VariableDeclaration, PtrType, Deref)

---

### Planned

* Full expression grammar
* Function bodies and scope handling
* Advanced type system
* Better diagnostics with line/column tracking
* Code generation (K → C++)

---

## Example

### Input (K)

```k
x:ptr(int) = *y

fn hello() {
}
```

---

### Internal Representation (AST)

```
VariableDeclaration(
  name = "x",
  type = PtrType("int"),
  value = Deref("y")
)

FunctionDeclaration(
  name = "hello",
  params = []
)
```

---

## Project Structure (Conceptual)

```
/lexer        == token generation
/parser       == AST construction
/ast          == node definitions
/transpiler   == C++ code generation
```

---

## Why Not Modify C++ Directly?

Modifying compilers like GCC or Clang is extremely complex.

K instead:

* acts as a frontend language
* reuses existing compiler infrastructure
* stays flexible and easier to iterate on

---

## Design Philosophy

* Minimal syntax noise
* Explicit types
* Predictable behavior
* Close-to-metal control
* Incremental complexity (start simple, grow gradually)

---

## Future Direction

K aims to evolve into a fully usable systems-level language with:

* Clean syntax
* Strong typing
* Modern diagnostics
* Efficient compilation via C++ backend

---

## License

This project is licensed under the terms specified in the LICENSE file.

## Author

Kairav

---