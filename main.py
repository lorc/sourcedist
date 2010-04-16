import graph
import pycparser

def main():
    ast = pycparser.parse_file("test1.c")
#    ast.show()
    gr1 = graph.FuncallGraph(ast);
    ast = pycparser.parse_file("test2.c")
    gr2 = graph.FuncallGraph(ast);

    for f1 in gr1.nodes:
        for f2 in gr2.nodes:
            print "%s and %s dist = %f"%\
                (f1.fname,f2.fname,lev_distance(f1.simple_ast.children
                                                ,f2.simple_ast.children))
#    f= "loopfunc"
#    f1= gr1.find_vertex("f1")
#    f2= gr2.find_vertex("recurs")
#    f1.simple_ast.show()
#    f2.simple_ast.show()
#    print lev_distance(f1.simple_ast.children,f2.simple_ast.children)

def lev_distance(s1,s2):
    "Calculate modified Levenshtein distance between two trees"
    
    if not s2:
        return len(s1)
    if not s1:
        return len(s2)

    D = [[None]*(len(s1)+1) for i in range(len(s2)+1)]
    for i in range(len(s1)+1):
        D[0][i] = float(i)
    for i in range(len(s2)+1):
        D[i][0] = float(i)
#    print "l1 = %d l2=%d"%(len(s1),len(s2))
    for x in range(len(s2)):
        for y in range(len(s1)):
#            print "(%d %d), (%s %s)"%(x,y,s2[x].type,s1[y].type)
            if (s1[y].children or s2[x].children) and\
                    s1[y].type == s2[x].type:
                dist = lev_distance(s1[y].children,s2[x].children)
            elif s1[y].type != s2[x].type:
                dist = 1.0
            else:
                dist = 0.0
            dist+=D[x][y]
            D[x+1][y+1] = min (dist,D[x][y+1]+1,
                               D[x][y+1]+1,D[x][y]+1)
    dist = D[len(s2)][len(s1)]

    # for y in range(len(s1)+1):
    #     s=""
    #     for x in range(len(s2)+1):
    #         s+= "%05.4f "%D[x][y]
    #     print s

    # print dist, max(len(s2),len(s1))
    return float(dist)/max(len(s2),len(s1))
            

if __name__=="__main__":
    main()
