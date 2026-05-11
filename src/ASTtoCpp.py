from parsingComponents.VariableParser import VariableDeclaration, Assignment, PtrType, Deref
from parsingComponents.FunctionParser import FunctionDeclaration, ReturnStatement
from parsingComponents.IfElseParser import IfStatement, ElseStatement
from parser import FunctionCall


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
    lines.append("#include <iostream>")
    lines.append("")
    body_lines = emit_body(AST, indent=0)
    for line in body_lines:
        lines.append(line)
        lines.append("")

    return lines