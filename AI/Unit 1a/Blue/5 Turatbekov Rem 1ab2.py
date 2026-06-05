import sys
from collections import deque

FILLED = "○"
EMPTY= "●"
i = int(sys.argv[1])
snode = FILLED*i+EMPTY+FILLED*(14-i)

def goal(s, i):
    return s[i]==FILLED and s.count(EMPTY)==14

def children(board):
    l = []
    for row, horiz in enumerate(board):
        for col, peg in enumerate(horiz):
            if peg==FILLED:
                moves = [(row, col-2), (row-2, col-2), (row-2, col), (row, col+2), (row+2, col+2), (row+2, col)]
                for m in moves:
                    r, c = m
                    if r>=0 and r<=4 and c>=0 and c<len(board[r]) and board[r][c]==EMPTY and board[mr:=(row+r)//2][mc:=(col+c)//2]==FILLED:
                        tmp = [list(i) for i in board]
                        tmp[row][col]=EMPTY
                        tmp[mr][mc]=EMPTY
                        tmp[r][c]=FILLED
                        tmp = "".join(["".join(i) for i in tmp])
                        l.append(tmp)
    return l

def boardlist(s):
    l = []
    ind = 0
    for i in range(5):
        l.append(s[ind:ind+i+1])
        ind+=i+1
    return l

def DFS(i):
    global snode
    fringe = deque()
    visited = set()
    fringe.append((snode, 1, [snode]))
    visited.add(snode)
    while fringe:
        node, steps, path = fringe.pop()
        if goal(node, i):
            return path
        for c in children(boardlist(node)):
            if c not in visited:
                tempPath = path.copy()
                tempPath.append(c)
                fringe.append((c, steps+1 , tempPath))
                visited.add(c)
    return None

def BFS(i):
    global snode
    fringe = deque()
    visited = set()
    fringe.append((snode, 1, [snode]))
    visited.add(snode)
    while fringe:
        node, steps, path = fringe.popleft()
        if goal(node, i):
            return path
        for c in children(boardlist(node)):
            if c not in visited:
                tempPath = path.copy()
                tempPath.append(c)
                fringe.append((c, steps+1 , tempPath))
                visited.add(c)
    return None

def printB(board):
    for i,v in enumerate(boardlist(board)):
        out = " "*(4-i)
        for i in v:
            out+=i+" "
        print(out)

dp, bp = DFS(i), BFS(i)

if not bp:
    print("No solution")
else:
    print("BFS:")
    for board in bp:
        printB(board)
        print()
    
    print("\nDFS:")
    for board in dp:
        printB(board)
        print()