import graph
import pycparser

def main():
    ast = pycparser.parse_file("test1.c")
#    ast.show()
    gr = graph.FuncallGraph(ast);

if __name__=="__main__":
    main()
