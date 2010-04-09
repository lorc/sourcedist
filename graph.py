from pycparser import c_ast

class GraphNode:
    "One node in function call graph. Will contain full and simplified AST"
    pass

class FuncallGraph:
    "Class that build and store function call graph. Every node contains AST for function"
    def __init__(self, ast):
        for ext in ast.ext:
            print ext
            if type(ext) == c_ast.FuncDef:
                ext.show()
        pass
    pass
