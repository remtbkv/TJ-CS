from collections import deque
import sys

def goal(v):
    return not "1" in v

def move(node, cube, dir, pi): # pi = pick_up_tile_index
    c = cube.copy()
    n, e, s, w, t, b = c["n"], c["e"], c["s"], c["w"], c["t"], c["b"]
    if dir==1: # north
        c["n"] = t
        c["t"] = s
        c["s"] = b
        c["b"] = n
    elif dir==2: # east
        c["e"] = t
        c["t"] = w
        c["w"] = b
        c["b"] = e
    elif dir==3: # south
        c["s"] = t
        c["t"] = n
        c["n"] = b
        c["b"] = s
    elif dir==4: # west
        c["w"] = t
        c["t"] = e
        c["e"] = b
        c["b"] = w
 
    if c["b"] and not int(node[pi]): # place down
        c["b"] = 0
        node[pi] = 1
    elif not c["b"] and int(node[pi]): # pick up
        c["b"] = 1
        node[pi] = 0

    return (node,c)

def children(node, cube):
    i, n, l = cube["pos"], int(len(node)**0.5), []
    row, col = i//n, i%n
    if row>0: #  move up
        l.append(move(node, cube, 1, i-n))
    if row+1<n: # move down
        l.append(move(node, cube, 3, i+n))
    if col>0: # move left
        l.append(move(node, cube, 4, i-1))
    if col+1<n: # move right
        l.append(move(node, cube, 2, i+1))
    return l

def BFS(snode, sindex):
    fringe = deque()
    visited = set()
    fringe.append(((snode, {"n": 0, "e": 0, "s": 0, "w": 0, "t": 0, "b": 0, "pos": sindex}), 0))
    visited.add(snode)
    while fringe:
        tup, steps = fringe.popleft()
        node, cube = tup
        if goal(node):
            return steps
        for c in children(node, cube):
            node, cube = c
            if node not in visited:
                fringe.append((c, steps+1))
                visited.add(c)
    return None

# fn = sys.argv[1]
fn = "cube_puzzles.txt"
with open(fn) as f:
    for ind, l in enumerate(f):
        lst = l.strip().split()
        board, index = lst[1], int(lst[2])
        board = board.replace(".", "0")
        board = board.replace("@", "1")
        print(board, index)
        steps = BFS(board, index)
        print(f"Line {ind}: {steps}")
        break