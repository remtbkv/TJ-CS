import sys
from collections import deque
from time import perf_counter


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

def kDFS(state, k):
    fringe = []
    fringe.append((state, 0, {state}))
    while fringe:
        node, depth, ancestors = fringe.pop()
        if goal(node):
            return depth
        if depth < k:
            for c in children(node):
                if c not in ancestors:
                    t = ancestors.copy()
                    t.add(c)
                    fringe.append((c, depth+1, t))
    return -1

def ID_DFS(snode):
    max_depth = 0
    result = -1
    while result < 0:
        result = kDFS(snode, max_depth)
        max_depth += 1
    return result

with open(sys.argv[1]) as f:
    for ind, val in enumerate(f):
        p = val.strip()
        d_start = perf_counter()
        if (steps := ID_DFS(p))>=0:
            d_t = perf_counter()-d_start
            d_out = str(steps) + " moves"
            b_start = perf_counter()
            b_out = str(BFS(p)) + " moves"
            b_t = perf_counter()-b_start
        else:
            out = "no solution"
        print(f"BFS: Line {ind}: {p}, {b_out} found in {b_t} seconds")
        print(f"ID_DFS: Line {ind}: {p}, {d_out} found in {d_t} seconds")