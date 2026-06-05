import sys
from time import perf_counter
from collections import deque

def goal(v):
    return v[:-1]=="".join(sorted(v)[1:])

def swap(i1, i2, node):
    a, b = min(i1, i2), max(i1, i2)
    return node[:a] + node[b] + node[a+1:b] + node[a] + node[b+1:]

def children(node):
    i, n, l = node.index("."), int(len(node)**0.5), []
    row, col = i//n, i%n
    if row>0: #  switch up
        l.append(swap(i-n, i, node))
    if row+1<n: # switch down
        l.append(swap(i+n, i, node))
    if col>0: # switch left
        l.append(swap(i-1, i, node))
    if col+1<n: # switch right
        l.append(swap(i+1, i, node))
    return l

def BFS(snode):
    fringe = deque()
    visited = set()
    fringe.append((snode, 0))
    visited.add(snode)
    while fringe:
        node, steps = fringe.popleft()
        if goal(node):
            return steps
        for c in children(node):
            if c not in visited:
                fringe.append((c, steps+1))
                visited.add(c)
    return None

def BiBFS(snode):
    enode = "".join(sorted(snode)[1:])+"."
    s_fringe, e_fringe = deque(), deque()
    s_fringe.append((snode, 0, [snode])), e_fringe.append((enode, 0, [enode]))
    s_visitDict, e_visitDict = dict(), dict()
    s_visitDict[snode], e_visitDict[enode] = 0, 0
    while s_fringe and e_fringe:
        s_node, s_steps, s_path = s_fringe.popleft()
        e_node, e_steps, e_path = e_fringe.popleft()
        for c in children(s_node):
            if c in e_visitDict:
                return s_steps+1+e_visitDict[c]
            if c not in s_visitDict:
                s_fringe.append((c, s_steps+1, s_path+[c]))
                s_visitDict[c]=s_steps+1
        for c in children(e_node):
            if c in s_visitDict:
                return e_steps+1+s_visitDict[c]
            if c not in e_visitDict:
                e_fringe.append((c, e_steps+1, e_path+[c]))
                e_visitDict[c]=e_steps+1
    return None

with open(sys.argv[1]) as f:
    for ind, val in enumerate(f):
        p = val.strip().split()[1]
        
        bfs_s = perf_counter()
        bfs = BFS(p)
        bfs_t = perf_counter()-bfs_s

        bi_s = perf_counter()
        bi = BiBFS(p)
        bi_t = perf_counter()-bi_s
        
        if bfs:
            bi_out, bfs_out = str(bi) + " moves", str(bfs) + " moves"
        else:
            bi_out = str(bi)
        print(f"BFS: Line {ind}: {p}, {bfs_out} found in {bfs_t} seconds")
        print(f"BiBFS: Line {ind}: {p}, {bi_out} found in {bi_t} seconds")
        print()
