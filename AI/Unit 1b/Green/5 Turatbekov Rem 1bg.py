import sys
from time import perf_counter
from heapq import heappush, heappop

def countPairs(board):
    p=0
    board = board.replace(".", "")
    if "A" in board:
        board = [ord(i) for i in board]
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if int(board[j])<int(board[i]):
                p+=1
    return p

def parity(board):
    n, p = int(pow(len(board), 0.5)), countPairs(board)
    r = board.index(".")//n
    if n%2==1:
        return p%2==0
    else:
        return r%2==0 and p%2==1 or r%2==1 and p%2==0

def taxi(board):
    d = 0
    n = int(pow(len(board), 0.5))
    if "A" in board:
        board = [ord(i)-64 if i!="." else i for i in board]
    for ind, val in enumerate(board):
        if val!=".":
            fr, fc = (int(val)-1)//n, (int(val)-1)%n
            cr, cc = ind//n, ind%n
            d+= abs(fr-cr)+abs(fc-cc)
    return d

def goal(v):
    return v[:-1]=="".join(sorted(v)[1:])

def swap(i1, i2, node):
    a, b = min(i1, i2), max(i1, i2)
    return node[:a] + node[b] + node[a+1:b] + node[a] + node[b+1:]

def children(node):
    i, n, l = node.index("."), int(len(node)**0.5), []
    row, col = i//n, i%n
    if row>0:
        l.append(swap(i-n, i, node))
    if row+1<n:
        l.append(swap(i+n, i, node))
    if col>0:
        l.append(swap(i-1, i, node))
    if col+1<n:
        l.append(swap(i+1, i, node))
    return l

def astar(snode):
    closed = set()
    node = (taxi(snode), 0, snode)
    fringe = []
    heappush(fringe, node)
    while fringe:
        t, steps, state = heappop(fringe)
        if goal(state):
            return steps
        if state not in closed:
            closed.add(state)
        for c in children(state):
            if c not in closed:
                temp = (steps+taxi(c), steps+1, c)
                heappush(fringe, temp)
    return None

with open(sys.argv[1]) as f:
    for ind, val in enumerate(f):
        b = val.strip().split()[1]
        start = perf_counter()
        if not parity(b):
            print(f"Line {ind}: {b}, A* - no solution determined in {perf_counter()-start} seconds")
        else:
            start = perf_counter()
            print(f"Line {ind}: {b}, A* - {astar(b)} moves in {perf_counter()-start} seconds")
