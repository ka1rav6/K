from parsingComponents.VariableParser import VariableDeclaration, Assignment, PtrType, Deref
from parsingComponents.FunctionParser import FunctionDeclaration, ReturnStatement
from parsingComponents.IfElseParser import IfStatement, ElseStatement
from parser import FunctionCall

def convert_string(s: str) -> str:
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        inner = s[1:-1]
        inner = inner.replace('"', '\\"')
        return f'"{inner}"'
    return s  # already double-quoted or not a string

def emit_expr(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return convert_string(value)
        return value

    if isinstance(value, Deref):
        return f"*{value.baseVar}"

    if isinstance(value, tuple) and len(value) == 2:
        kind, val = value
        if kind == "STRING":
            return convert_string(str(val))
        if kind == "NUMBER":
            return str(val)
        if kind in ("IDENT", "KEYWORD"):
            if val == "true":
                return "true"
            if val == "false":
                return "false"
            return str(val)
        return str(val)

    if isinstance(value, VariableDeclaration):
        return emit_var(value, indent=0).rstrip(";\n ")
    if isinstance(value, Assignment):
        return emit_assignment(value, indent=0).rstrip(";\n ")

    if isinstance(value, list):
        parts = []
        for tok in value:
            parts.append(emit_expr(tok))
        return " ".join(parts)
    return str(value)

def emit_var(node: VariableDeclaration, indent: int) -> str:
    """Emit a variable declaration as a C++ line."""
    pad = "    " * indent
    if isinstance(node.type, PtrType):
        type_str = f"{node.type.base}*"
    else:
        type_str = str(node.type)
    if node.value is not None:
        val_str = emit_expr(node.value)
        return f"{pad}{type_str} {node.name} = {val_str};"
    else:
        return f"{pad}{type_str} {node.name};"

def emit_assignment(node: Assignment, indent: int) -> str:
    """Emit a variable reassignment."""
    pad = "    " * indent
    val_str = emit_expr(node.value)
    return f"{pad}{node.name} = {val_str};"

def emit_function_call(node: FunctionCall, indent: int) -> str:

    pad = "    " * indent
    if node.name == "cout":
        parts = [emit_expr(a) for a in node.args]
        chain = " << ".join(parts)
        return f"{pad}std::cout << {chain};"
    if node.name == "cin":
        parts = [emit_expr(a) for a in node.args]
        chain = " >> ".join(parts)
        return f"{pad}std::cin >> {chain};"

    args_str = ", ".join(emit_expr(a) for a in node.args)
    return f"{pad}{node.name}({args_str});"

def emit_return(node: ReturnStatement, indent: int) -> str:
    pad = "    " * indent
    val_str = emit_expr(node.value)
    return f"{pad}return {val_str};"

def emit_body(nodes: list, indent: int) -> list[str]:

    lines = []
    prev = None
    for node in nodes:
        if isinstance(node, IfStatement) and isinstance(prev, (IfStatement, ElseStatement)):
            code = emit_if(node, indent, keyword="else if")
            lines[-1] = lines[-1] + " " + code.lstrip()
        elif isinstance(node, ElseStatement) and isinstance(prev, IfStatement):
            code = emit_else(node, indent)
            lines[-1] = lines[-1] + " " + code.lstrip()
        else:
            lines.append(emit_node(node, indent))
        prev = node
    return lines


def emit_if(node: IfStatement, indent: int, keyword: str = "if") -> str:

    pad = "    " * indent
    cond_str = emit_expr(node.condition)
    lines = [f"{pad}{keyword} ({cond_str}) {{"]
    lines.extend(emit_body(node.content, indent + 1))
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def emit_else(node: ElseStatement, indent: int) -> str:
    """Emit an else block."""
    pad = "    " * indent
    lines = [f"{pad}else {{"]
    lines.extend(emit_body(node.content, indent + 1))
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def emit_function(node: FunctionDeclaration, indent: int) -> str:
    pad = "    " * indent

    params = []
    for p in node.params:
        if isinstance(p.type, PtrType):
            type_str = f"{p.type.base}*"
        else:
            type_str = str(p.type)
        params.append(f"{type_str} {p.name}")
    params_str = ", ".join(params)

    if node.name == "main":
        ret_type = "int"
    else:
        ret_type = "auto"
    lines = [f"{pad}{ret_type} {node.name}({params_str}) {{"]
    lines.extend(emit_body(node.content, indent + 1))

    if node.name == "main":
        has_return = any(isinstance(c, ReturnStatement) for c in node.content)
        if not has_return:
            lines.append(f"{pad}    return 0;")
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def emit_node(node, indent: int) -> str:

    if isinstance(node, FunctionDeclaration):
        return emit_function(node, indent)
    if isinstance(node, VariableDeclaration):
        return emit_var(node, indent)
    if isinstance(node, Assignment):
        return emit_assignment(node, indent)
    if isinstance(node, FunctionCall):
        return emit_function_call(node, indent)
    if isinstance(node, ReturnStatement):
        return emit_return(node, indent)
    if isinstance(node, ElseStatement):
        return emit_else(node, indent)
    if isinstance(node, IfStatement):
        return emit_if(node, indent)
    raise TypeError(f"Unknown AST node type: {type(node).__name__}")


def to_cpp(AST: list) -> list | None:
    if not AST:
        return None
    lines: list[str] = []
    lines.append("#include <iostream>\n\n")
    lines.append("")
    body_lines = emit_body(AST, indent=0)
    for line in body_lines:
        lines.append(line)
        lines.append("")

    return lines