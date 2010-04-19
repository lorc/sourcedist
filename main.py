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
            dist,order = lev_distance(f1.simple_ast.children
                                      ,f2.simple_ast.children)
            print "%s and %s dist = %d from %d (%05.2f%% match))"%\
                (f1.fname,f2.fname,dist,order,(float(1) - float(dist)/order)*100)

#    f= "loopfunc"
#    f1= gr1.find_vertex(f)
#    f2= gr2.find_vertex(f)
#    f1.simple_ast.show()
#    f2.simple_ast.show()
#    print lev_distance(f1.simple_ast.children,f2.simple_ast.children)

def lev_distance(s1,s2):
    "Calculate modified Levenshtein distance between two trees"
    
    D = [[0]*(len(s1)+1) for i in range(len(s2)+1)]

    for i in range(1,len(s1)+1):
        D[0][i] = D[0][i-1] + s1[i-1].order
    for i in range(1,len(s2)+1):
        D[i][0] = D[i-1][0] + s2[i-1].order
#    print "l1 = %d l2=%d"%(len(s1),len(s2))

    for x in range(len(s2)):
        for y in range(len(s1)):
#            print "(%d %d), (%s %s)"%(x,y,s2[x].type,s1[y].type)
            if (s1[y].children or s2[x].children) and\
                    s1[y].type == s2[x].type:
                dist,order = lev_distance(s1[y].children,s2[x].children)
            elif s1[y].type != s2[x].type:
                dist = max(s1[y].order,s2[x].order)
            else:
                dist = 0.0
            dist+=D[x][y]
            D[x+1][y+1] = min (dist,
                               D[x][y+1]+s2[x].order,
                               D[x+1][y]+s1[y].order,
                               D[x][y]+abs(s2[x].order-s1[y].order))
    dist = D[len(s2)][len(s1)]

    # for y in range(len(s1)+1):
    #     s=""
    #     for x in range(len(s2)+1):
    #         s+= "%05.4f "%D[x][y]
    #     print s

    # print dist, max(D[0][len(s1)],D[len(s2)][0])
    return dist,max(reduce(lambda x,y:x + y.order,s1,0), reduce(lambda x,y:x + y.order,s2,0),dist )
            


if __name__=="__main__":
    main()
