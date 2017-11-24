# - * - coding:utf-8 - * - -
from pygraph.classes.digraph import digraph
from math import *
import LoadData
from guppy import hpy
from datetime import datetime
f_authority=open('data/authority.txt','w')
f_hub = open('data/hub.txt','w')
class HITSIterator:
    __doc__ = '''hub,authority'''

    def __init__(self, dg):
        self.max_iterations = 100 # maximun iteration times
        self.min_delta = 0.0001  # epsilon
        self.graph = dg

        self.hub = {}
        self.authority = {}
        for node in self.graph.nodes():
            self.hub[node] = 1
            self.authority[node] = 1

    def hits(self):
        if not self.graph:
            return

        flag = False
        for i in range(self.max_iterations):
            change = 0.0  # 记录每轮的变化值
            norm = 0  # 标准化系数
            # To Calculate the authority value of each page
            tmp = self.authority.copy() #deep copy
            for node in self.graph.nodes():
                self.authority[node] = 0
                for incident_page in self.graph.incidents(node):  # all in pages
                    self.authority[node] += self.hub[incident_page]
                norm += pow(self.authority[node], 2)
            # Standardize
            norm = sqrt(norm)
            for node in self.graph.nodes():
                self.authority[node] /= norm
                change += abs(tmp[node] - self.authority[node])

            # To Calculate the hub value of each page
            norm = 0
            tmp = self.hub.copy()
            for node in self.graph.nodes():
                self.hub[node] = 0
                for neighbor_page in self.graph.neighbors(node):  # 遍历所有“出射”的页面
                    self.hub[node] += self.authority[neighbor_page]
                norm += pow(self.hub[node], 2)

            # Standardize
            norm = sqrt(norm)
            for node in self.graph.nodes():
                self.hub[node] /= norm
                change += abs(tmp[node] - self.hub[node])

            print("This is NO.%s iteration" % (i + 1))

            if change < self.min_delta: # Stop the iteration
                flag = True
                break

        if flag:
            print("finished in %s iterations!" % (i + 1))
        else:
            print("finished out of 100 iterations!")

        for line in sorted(self.authority.items(),key=lambda x:x[1],reverse=True)[0:100]:
            #print line
            f_authority.write(str(line[0])+' '+str(line[1])+'\n')

        for line in sorted(self.hub.items(), key=lambda x: x[1],reverse=True)[0:100]:
            f_hub.write(str(line[0]) + ' ' + str(line[1]) + '\n')

if __name__ == '__main__':

    dg = digraph()
    start = datetime.now()
    dg.add_nodes(LoadData.nodes)
    print 'Add nodes use %s seconds' %(datetime.now()-start).seconds
    start = datetime.now()
    for edge in LoadData.edges:
        dg.add_edge(edge)
    print hpy().heap()
    print 'Add edges use %s seconds' % (datetime.now() - start).seconds
    start = datetime.now()
    hits = HITSIterator(dg)
    hits.hits()
    print 'Runtime %s seconds' % (datetime.now() - start).seconds
    f_authority.close()
    f_hub.close()

