__author__ = 'xanxus'
nodeNum, edgeNum = 0, 0
arcs = []
 
 
class Arc(object):
    def __init__(self):
        self.src = -1
        self.dst = -1
        self.cap = -1
 
 
s, t = -1, -1
with open('sample.dimacs') as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith('p'):
            tokens = line.split(' ')
            nodeNum = int(tokens[2])
            edgeNum = tokens[3]
        if line.startswith('n'):
            tokens = line.split(' ')
            if tokens[2] == 's':
                s = int(tokens[1])
            if tokens[2] == 't':
                t = int(tokens[1])
        if line.startswith('a'):
            tokens = line.split(' ')
            arc = Arc()
            arc.src = int(tokens[1])
            arc.dst = int(tokens[2])
            arc.cap = int(tokens[3])
            arcs.append(arc)
 
nodes = [-1] * nodeNum
for i in range(s, t + 1):
    nodes[i - s] = i
adjacent_matrix = [[0 for i in range(nodeNum)] for j in range(nodeNum)]
forward_matrix = [[0 for i in range(nodeNum)] for j in range(nodeNum)]
for arc in arcs:
    adjacent_matrix[arc.src - s][arc.dst - s] = arc.cap
    forward_matrix[arc.src - s][arc.dst - s] = arc.cap
flow_matrix = [[0 for i in range(nodeNum)] for j in range(nodeNum)]
 
height = [0] * nodeNum
height[0] = nodeNum
for i in range(len(adjacent_matrix)):
    flow_matrix[0][i] = adjacent_matrix[0][i]
    adjacent_matrix[0][i] = 0
    adjacent_matrix[i][0] = flow_matrix[0][i]
 
 
def excess(v):
    in_flow, out_flow = 0, 0
    for i in range(len(flow_matrix)):
        in_flow += flow_matrix[i][v]
        out_flow += flow_matrix[v][i]
    return in_flow - out_flow
 
 
def exist_excess():
    for v in range(len(flow_matrix)):
        if excess(v) > 0 and v != t - s:
            return v
    return None
 
 
v = exist_excess()
while v:
    has_lower_height = False
    for j in range(len(adjacent_matrix)):
        if adjacent_matrix[v][j] != 0 and height[v] > height[j]:
            has_lower_height = True
            if forward_matrix[v][j] != 0:
                bottleneck = min([excess(v), adjacent_matrix[v][j]])
                flow_matrix[v][j] += bottleneck
                adjacent_matrix[v][j] -= bottleneck
                adjacent_matrix[j][v] += bottleneck
            else:
                bottleneck = min([excess(v), flow_matrix[j][v]])
                flow_matrix[j][v] -= bottleneck
                adjacent_matrix[v][j] -= bottleneck
                adjacent_matrix[j][v] += bottleneck
    if not has_lower_height:
        height[v] += 1
    v = exist_excess()
for arc in arcs:
    print('f %d %d %d' % (arc.src, arc.dst, flow_matrix[arc.src - s][arc.dst - s]))