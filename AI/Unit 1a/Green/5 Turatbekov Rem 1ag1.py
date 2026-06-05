import sys

def print_puzzle(board, n):
    n = int(pow(n, 0.5))
    return "\n".join([" ".join(board[i*n:i*n+n]) for i in range(n)])

def find_goal(board):
    return "".join(s := sorted(board))[1:]+s[0]

def swap(i1, i2, node):
    a, b = min(i1, i2), max(i1, i2)
    return node[:a] + node[b] + node[a+1:b] + node[a] + node[b+1:]

def get_children(node):
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

with open(sys.argv[1]) as f:
    for ind, val in enumerate(f):
        p = val.strip().split()[1]
        s = print_puzzle(p, len(p))
        g = find_goal(p)
        c = get_children(p)
        print(f"Line {ind} start state:\n{s}\nLine {ind} goal state: {g}\nLine {ind} children: {c}\n")