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

with open(sys.argv[1]) as f:
    for ind, val in enumerate(f):
        start = perf_counter()
        p = val.strip().split()[1]
        if (steps := BFS(p)):
            out = str(steps) + " moves"
        else:
            out = "no solution"
        t = perf_counter()-start
        print(f"Line {ind}: {p}, {out} found in {t} seconds")
