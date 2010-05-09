import sys
import graph
import pycparser
from optparse import OptionParser

def get_parsed(filename):
    ast = pycparser.parse_file(filename)
    dump_ast(filename,ast)
    gr = graph.FuncallGraph(ast);
    gr.dump_sast(filename)
    return gr

def dump_ast(source_file,ast):
    fname  = source_file + ".ast"
    f = open(fname,"w")
    ast.show(buf = f)
    f.close()

def compare_two_files(file1,file2,logfile=sys.stdout):
    gr1 = get_parsed(file1)
    gr2 = get_parsed(file2)
    correspondence = get_coresspond_functions(gr1.nodes,gr2.nodes)
    totaldist=0
    totalord=0
    for func,corfunc, metr in correspondence:
        if corfunc != None:
            logfile.write( "%s corresponds %s with %05.2f%% similarity\n"%\
                (func.fname,corfunc.fname,(float(1) - float(metr[0])/metr[1])*100))
        else:
            logfile.write( "Not found corresponding function to '%s'\n"%func.fname)
        totaldist += metr[0]
        totalord  += metr[1]

    logfile.write("Total file match = %05.2f%%"%((float(1) - float(totaldist)/totalord)*100))
    return (totaldist,totalord,correspondence)
    
def compare_one_to_many(file1,file_list, logfile=sys.stdout):
    results = []
    for f in file_list:
        logfile.write("Comparing %s and %s:\n\n"%(file1,f))
        results.append(compare_two_files(file1,f,logfile))

    pass

def main():
    parser = OptionParser("usage: %prog [-i list_file|-f file1] file2")
    parser.add_option("-f","--file", dest="file1", help="compare FILE1 to file2")
    parser.add_option("-i","--list", dest="list", help="read file list from LIST")
    parser.add_option("-l","--log", dest="log", help="write output to LOG")
    
    (options,args)=parser.parse_args()
    
    if len(args) != 1:
        parser.error("incorrent number of input files")
    if options.file1 and options.list:
        parser.error("options LIST and FILE1 are mutually exclusive")
    if not options.file1 and not options.list:
        parser.error("must be provided FILE1 or LIST")
    
    logfile = sys.stdout
    
    if options.log:
        logfile = open(options.log,"wt")
    if options.file1:
        compare_two_files(options.file1,args[0],logfile)
    if options.list:
        pass
    
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
