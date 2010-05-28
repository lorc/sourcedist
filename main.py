import sys
import graph
import pycparser
import sast_import
from optparse import OptionParser
from time import time

def get_parsed(filename,simple = False):
    if not simple:
        ast = pycparser.parse_file(filename)
        dump_ast(filename,ast)
        gr = graph.FuncallGraph(ast);
        gr.dump_sast(filename)
        return gr
    else:
        fsast = open(filename,"r")
        text = fsast.read()
        fsast.close()
        gr = sast_import.read_graph(text)
        gr.dump_sast(filename)
        return gr

def dump_ast(source_file,ast):
    fname  = source_file + ".ast"
    f = open(fname,"w")
    ast.show(buf = f)
    f.close()

def compare_two_files(file1, file2, logfile=sys.stdout, cycles=1, simple = False):

    gr1 = get_parsed(file1,simple)
    gr2 = get_parsed(file2,simple)

    ts = time()

    for i in xrange(cycles):
        correspondence = get_coresspond_functions(gr1.nodes,gr2.nodes)
    
    te = time()
   
    totaldist=0
    totalord=0
    for func,corfunc, metr in correspondence:
        if corfunc != None:
            logfile.write( "%-20s corresponds %-20s with %05.2f%% similarity\n"%\
                (func.fname,corfunc.fname,(float(1) - float(metr[0])/metr[1])*100))
        else:
            logfile.write( "Not found corresponding function to '%s'\n"%func.fname)
        totaldist += metr[0]
        totalord  += metr[1]
    if totalord != 0:
        logfile.write("Total file match = %05.2f%%\n"%((float(1) - float(totaldist)/totalord)*100))
    else:
        logfile.write("Total file match = 0%")
    if cycles>1:
        logfile.write("%d cycles took %f010 seconds\n"%(cycles,(te-ts)))
    
    return (totaldist,totalord,correspondence,file2)
    
def compare_one_to_many(file1, file_list, logfile=sys.stdout, cycles=1):
    results = []
    for f in file_list:
        logfile.write("\nComparing %s and %s:\n"%(file1,f))
        results.append(compare_two_files(file1,f,logfile,cycles))
    results.sort(cmp = lambda y,x:cmp((float(1) - float(x[0])/x[1]),(float(1) - float(y[0])/y[1])))
    logfile.write("\nBest match files (score over 75%)\n")
   
    for tdist,tord,cor,fname in results:
        score = (float(1) - float(tdist)/tord) 
        if  score >= 0.75:
            logfile.write( "%s \tscore: %05.2f%%\n"%(fname,score*100)) 
        
    pass

def main():
    parser = OptionParser("usage: %prog [options] (-i list_file|-f file1| -s file1) file2")
    parser.add_option("-f","--file", dest="file1", help="compare FILE1 to file2")
    parser.add_option("-s","--sast", dest="sast", help="compare SAST structure FILE1 to file2")
    parser.add_option("-i","--list", dest="list", help="read file list from LIST")
    parser.add_option("-l","--log", dest="log", help="write output to LOG")
    parser.add_option("-k","--cycles", dest="cycles", 
                      help="run CYCLES of compare and print time",
                      type="int",default=1)
    (options,args)=parser.parse_args()
    
    if len(args) != 1:
        parser.error("incorrent number of input files")
    if (options.file1 and options.list) or \
            (options.file1 and options.sast) or \
            (options.list and options.sast):
        parser.error("options LIST, SAST and FILE1 are mutually exclusive")
    if not options.file1 and not options.list and not options.sast:
        parser.error("must be provided FILE1, SAST, or LIST")
    
    logfile = sys.stdout
    
    if options.log:
        logfile = open(options.log,"wt")
    if options.file1:
        compare_two_files(options.file1,args[0],logfile,options.cycles)
    if options.list:
        flist = open(options.list,"r")
        files = [f.strip() for f in flist.readlines()]
        flist.close()
        compare_one_to_many(args[0],files,logfile,options.cycles)
    if options.sast:
        compare_two_files(options.sast,args[0],logfile,options.cycles,True)

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

#    for y in range(len(s1)+1):
#        s=""
#        for x in range(len(s2)+1):
#            s+= "%05.4f "%D[x][y]
#        print s
    
    rord = max(reduce(lambda x,y:x + y.order,s1,0), reduce(lambda x,y:x + y.order,s2,0),dist )
    if dist>rord:
        rord = dist
#    print "DIST",dist,rord
    return dist,rord

def get_correspond_function(func, flist):
    dist = float(0)
    corfunc = None
    metr=(0,0)
    for f in flist:
        cur,order = lev_distance(func.simple_ast.children,f.simple_ast.children)
        if order!=0:
            newdist = (float(1) - float(cur)/order)
        else:
            newdist = 1
        if newdist>dist:
            corfunc = f
            dist = newdist
            metr = cur,order
#    if dist>=0.5:
    return (corfunc, metr)

def get_coresspond_functions(flist1,flist2):
    cor = []
    for x in flist1:
        ret =  get_correspond_function(x,flist2)
        if ret:
            cor.append((x,ret[0],ret[1]))
     
    return cor
        
if __name__=="__main__":
    main()
