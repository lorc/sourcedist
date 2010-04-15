from pycparser import c_ast
from minimize_ast import MinimizeAst
class GraphNode:
    "One node in function call graph. Will contain full and simplified AST"    
    def __init__(self,ast):
        self.full_ast = ast
        self.simple_ast = MinimizeAst(ast)
        self.fname = ast.decl.name
        self.edges = []
        print "Added function", self.fname
        self.simple_ast.show()

    def add_edge(self,f):
        self.edges.append(f)

class FuncallGraph:
    "Class that build and store function call graph. Every node contains AST for function"
    def funcall_visitor(self, ast,parent):
        if type(ast) == c_ast.FuncCall:
            parent.add_edge(self.find_vertex(ast.name.name))
        else:
            for c in ast.children():
                self.funcall_visitor(c,parent)
                
    def find_vertex(self,fname):
        for f in self.nodes:
            if f.fname == fname:
                return f
        return None

    def dump(self):
        print "Call graph:"
        for f in self.nodes:
            if len(f.edges):
                print " %s calls:"%f.fname
                for f2 in f.edges:
                    print "   %s"%f2.fname
            else:
                print " %s calls none"%f.fname

    def __init__(self, ast):
        self.nodes = []
        #first pass - get all functions
        for ext in ast.ext:
            if type(ext) == c_ast.FuncDef:
                self.nodes.append(GraphNode(ext))
        #second pass: find functioncalls
        for f in self.nodes:
            self.funcall_visitor(f.full_ast,f)
        self.dump()
