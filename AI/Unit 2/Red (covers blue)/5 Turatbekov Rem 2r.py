import sys

def goal(board):
    return board and len("".join(board))==len(board)

def get_sorted_values(board, index):
    return board[index]

def get_most_constrained_var(board):
    ind, least = 0, 100
    for i, posIndices in enumerate(board):
        if (l:=len(posIndices))>1 and l<least:
            ind, least = i, l
    return ind

def forward_looking(board, solved):
    allsolved = set()
    if goal(board):
        return board
    if not solved:
        solved = [(ind,val) for ind,val in enumerate(board) if len(val)==1]
    allsolved.update([x[0] for x in solved])
    while solved:
        ind, val = solved.pop()
        for ci in neighbor_set[ind]:
            v = board[ci] = board[ci].replace(val,'')
            if not v:
                return None
            if len(v)==1 and ci not in allsolved and (ci, v) not in solved:
                solved.append((ci, v))
                allsolved.add(ci)
    return board

def constraint_propogation(board):
    if not board:
        return None
    if goal(board):
        return board
    for ind in range(N**2):
        for cset in [row_constraint[ind//N], col_constraint[ind % N], sub_constraint[ind]]:
            possibles = {i: (0, -1) for i in symbol_set}
            for ci in cset:
                if not board[ci]:
                    return None
                for v in board[ci]:
                    possibles[v] = (possibles[v][0]+1, ci)
            for v, n in possibles.items():
                if n[0] == 0:
                    return None
                if n[0] == 1 and len(board[n[1]]) != 1:
                    board[n[1]] = v
    return board

def csp_backtracking(board):
    if goal(board):
        return board
    var = get_most_constrained_var(board)
    for val in get_sorted_values(board, var):
        nb = board.copy()
        nb[var] = val
        nb = forward_looking(nb, [(var, val)])
        nb = constraint_propogation(nb)
        if nb:
            nb = csp_backtracking(nb)
            if nb:
                return nb
    return None

def display(board):
    sep = "-"*((nW*2)+1 + 2*subblock_width*nW)+"\n"
    a = sep
    for nr in range(nH):
        for r in range(subblock_height):
            a+="| "
            for nc in range(nW):
                for c in range(subblock_width):
                    a+= board[nr*subblock_height*N+r*N+nc*subblock_width+c]+" "
                a+="| "
            a+="\n"
        a+=sep
    print(a)

def read_puzzles(filename):
    with open(filename) as f:
        for l in f:
            B = l.strip()
            global N, nW, nH, subblock_height, subblock_width, symbol_set, row_constraint, col_constraint, sub_constraint, neighbor_set
            N = 0
            subblock_height = 0
            subblock_width = 0
            symbol_set = ""
            row_constraint = {}
            col_constraint = {}
            sub_constraint = {}
            neighbor_set = {}
            N=int(pow(len(B),0.5))
            for n in range(1, N+1):
                if n < 10:
                    symbol_set += str(n)
                else:
                    symbol_set += chr(n+55)
            board = ["".join([i for i in symbol_set]) if val == "." else val for val in B]
            if (n := int(pow(N,0.5)))==pow(N,0.5):
                subblock_width = n
                subblock_height = n
            else:
                for w in range(int(pow(N, 0.5))+1, N+1):
                    if N%w==0:
                        subblock_width = w
                        break
                subblock_height = N//subblock_width
            nW, nH = N//subblock_width, N//subblock_height
            for r in range(N):
                row_constraint[r] = [i for i in range(r*N,r*N+N)]
            for c in range(N):
                col_constraint[c] = [i for i in range(c,N**2,N)]
            sub={}
            for nr in range(nH):
                for r in range(subblock_height):
                    for nc in range(nW):
                        for c in range(subblock_width):
                            block, i = (nr, nc), nr*subblock_height*N+r*N+nc*subblock_width+c
                            if block in sub:
                                sub[block] = sub[block]+[i]
                            else:
                                sub[block] = [i]
            for n in range(N**2):
                nr = n//(subblock_width*subblock_height*nW)
                nc = n%N//subblock_width
                sub_constraint[n] = sub[(nr,nc)]
                r = n//N
                c = n%N
                neighbor_set[n] = {i for i in (row_constraint[r]+col_constraint[c]+sub_constraint[n]) if i!=n}
            board = forward_looking(board, [])
            s = "".join(csp_backtracking(board))
            print(s)
            # check valid
            # us = set(tuple(i) for i in sub_constraint.values())
            # csets = list(row_constraint.values())+list(col_constraint.values()) + [list(i) for i in us]
            # print(checkBoard(s, csets))

def checkBoard(state, csets):
    for cset in csets:
        for i in symbol_set:
            if [state[i] for i in cset].count(i)>1:
                return False
    return True

fn = sys.argv[1]
read_puzzles(fn)