import sys
import graph
import pycparser

def dump_ast(source_file,ast):
    fname  = source_file + ".ast"
    f = open(fname,"w")
    ast.show(buf = f)
    f.close()

def compare_two_files(file1,file2,logfile=None):
    ast = pycparser.parse_file(file1)
    dump_ast(file1,ast)
#    ast.show()
    gr1 = graph.FuncallGraph(ast);
    ast = pycparser.parse_file(file2)
    dump_ast(file2,ast)
    gr2 = graph.FuncallGraph(ast);
    gr1.dump_sast(file1)
    gr2.dump_sast(file2)
    correspondence = get_coresspond_functions(gr1.nodes,gr2.nodes)
    totaldist=0
    totalord=0
    for func,corfunc, metr in correspondence:
        if corfunc != None:
            print "%s corresponds %s with %05.2f%% similarity"%\
                (func.fname,corfunc.fname,(float(1) - float(metr[0])/metr[1])*100)
        else:
            print "Not found corresponding function to '%s'"%func.fname
        totaldist += metr[0]
        totalord  += metr[1]

    print "Total file match = %05.2f%%"%((float(1) - float(totaldist)/totalord)*100)
    
    

def main():

    if len(sys.argv) == 3:
        compare_two_files(sys.argv[1],sys.argv[2])
    elif len(sys.argv)==4 and sys.argv[1] == "-i" :
        pass
    else:
        print "Usage:\n %s <input_file1> <input_file2>\nor\n %s -i <listfile> <input_file>"%(sys.argv[0],sys.argv[0])
        return
   
  
#    for f1 in gr1.nodes:
#        for f2 in gr2.nodes:
#            dist,order = lev_distance(f1.simple_ast.children
#                                      ,f2.simple_ast.children)
#            print "%s and %s dist = %d from %d (%05.2f%% match))"%\
#                (f1.fname,f2.fname,dist,order,(float(1) - float(dist)/order)*100)
#    f= "loopfunc"
#    f1= gr1.find_vertex("f1")
#    f2= gr2.find_vertex("rename_f2")
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

def get_correspond_function(func, flist):
    dist = float(0)
    corfunc = None
    metr=(0,0)
    for f in flist:
        cur,order = lev_distance(func.simple_ast.children,f.simple_ast.children)
        newdist = (float(1) - float(cur)/order)
        if newdist>dist:
            corfunc = f
            dist = newdist
            metr = cur,order
    if dist>=0.5:
        return corfunc, metr
    return None

def get_coresspond_functions(flist1,flist2):
    cor = []
    for x in flist1:
        corfunct,metr = get_correspond_function(x,flist2)
        cor.append((x,corfunct,metr))
    return cor
        
if __name__=="__main__":
    main()
