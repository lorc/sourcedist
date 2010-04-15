import sys
from pycparser import c_parser,c_ast

class SimpleAstNode:
    "Represents one node in simple AST"
    def __init__(self,node_type):
        self.type = node_type #node name
        self.children = []

    def show(self, offset=0):
        print " " * offset,self.type
        for child in self.children:
            child.show(offset+2)


def MinimizeAst(full_ast):
    "Function used to remove all unnecessary data from AST (leave only control structures and function calls)"
    res = []
    for child in full_ast.children():
        new = MinimizeAst(child)
        if new:
            if type(new) != list:
                res.append(new)
            else:
                res.extend(new)
    node = None
    if type(full_ast) == c_ast.If:
        node = SimpleAstNode("if")
    elif type(full_ast) == c_ast.For or \
            type(full_ast) == c_ast.While or\
            type(full_ast) == c_ast.DoWhile:
        node = SimpleAstNode("loop")
    elif type(full_ast) == c_ast.Switch:
        node = SimpleAstNode("switch")
    elif  type(full_ast) == c_ast.Continue or \
            type(full_ast) == c_ast.Break or \
            type(full_ast) == c_ast.Goto or \
            type(full_ast) == c_ast.Return:
        node = SimpleAstNode("jump")
    elif type(full_ast) == c_ast.FuncCall:
        node = SimpleAstNode("funcall")
    elif type(full_ast) ==c_ast.FuncDef:
        node = SimpleAstNode("funcdef")
    
    if node:
        node.children.extend(res)
        return node
    return res
