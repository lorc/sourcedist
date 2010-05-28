import sys
from minimize_ast import *
import graph

class lines_tokenizer:
    def __init__(self,string):
        self.lines = string.split("\n")
        self.cur_pos = 0
    
    def peek(self):
        if len(self.lines)>self.cur_pos:
            return self.lines[self.cur_pos]
        return None
    
    def proceed(self):
        self.cur_pos+=1

def count_spaces(string):
    ret = 0
    for s in string:
        if s==" ":
            ret+=1
        else:
            break
    return ret

def create_sast(tokenizer,level,name,step=0):
    #print "Level = %d lines=%s name = %s"%(level,str(lines),name) 

    ret = SimpleAstNode(name)

    while True:
        l = tokenizer.peek()
        if not l:
            break

        if step == 0:
            step = count_spaces(l)

        if not l.strip():
            tokenizer.proceed()
            continue
        
        spaces = count_spaces(l)
        if spaces % step != 0:
            raise Exception("indendation error: " + l)
        
        cur_level = spaces/step
      #  print "levels",l,level,cur_level
        if cur_level<level:
            return ret
        
        if cur_level>level+1:
            raise Exception("indendation level error: " + l)
        
        tokenizer.proceed()
        ret.children.append(create_sast(tokenizer,level+1,
                                        l.strip().split()[0],step))
    #print "last = " + lines[0]
    return ret
def read_graph(data):
 
    tokenizer = lines_tokenizer(data)
    g = graph.FuncallGraph()
 
    while True:
        l = tokenizer.peek()
        if not l:
            break
       
        if not l.strip():
            tokenizer.proceed()
            continue
        if l[0]==' ':
            raise Exception("Not a function: " + l)
        f = graph.GraphNode()
        f.fname = l
        tokenizer.proceed()
        sa = create_sast(tokenizer,1,"")
        f.simple_ast = sa.children[0]
        f.simple_ast.calc_order()
#        print f.fname
 #       f.simple_ast.show(2)
        g.nodes.append(f)
    return g
