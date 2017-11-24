from datetime import datetime
start = datetime.now()
os_path = 'data/'
f_handle = open(os_path+'web-Google.txt')
content = f_handle.readlines()[4:1000]

nodesdict={}
edges=[]
for line in content:
    line=line.strip('\n').split()
    nodesdict.setdefault(line[0],0)
    nodesdict.setdefault(line[1], 0)
    edges.append((line[0],line[1]))
nodes=nodesdict.keys()
num = len(edges)
edges = list(set(edges))
print 'Number of Nodes is: %d.' % len(nodes)
print 'Number of Edges is: %d, including %d repeated Edges' % (num,num-len(edges))
print 'Data Loading Module use %d seconds.' % (datetime.now()-start).seconds
