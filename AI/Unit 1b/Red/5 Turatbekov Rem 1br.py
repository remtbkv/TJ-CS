import sys
from time import perf_counter
from heapq import heappush, heappop
from itertools import permutations


def taxi(board):
    d = 0
    for ind, val in enumerate(board):
        if val != ".":
            fr, fc = tdct[val]
            cr, cc = ind // N, ind % N
            d += abs(fr - cr) + abs(fc - cc)
    return d


def goal_korf(v):
    return v == ".ABCDEFGHIJKLMNO"


def goal(v):
    if len(v) == 16:
        return v == "ABCDEFGHIJKLMNO."
    elif len(v) == 25:
        return v == "ABCDEFGHIJKLMNOPQRSTUVWX."


def countPairs(board):
    p = 0
    board = board.replace(".", "")
    if "A" in board:
        board = [ord(i) for i in board]
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if int(board[j]) < int(board[i]):
                p += 1
    return p


def parity(board):
    n, p = int(pow(len(board), 0.5)), countPairs(board)
    r = board.index(".")//n
    if n % 2 == 1:
        return p % 2 == 0
    else:
        return r % 2 == 0 and p % 2 == 1 or r % 2 == 1 and p % 2 == 0


def swap(i1, i2, node):
    n = list(node)
    n[i1], n[i2] = n[i2], n[i1]
    return "".join(n)


def children(node):
    i, l = node.index("."), []
    row, col = i//N, i % N
    if row > 0:  # up
        l.append(swap(i-N, i, node))
    if row+1 < N:  # down
        l.append(swap(i+N, i, node))
    if col > 0:  # left
        l.append(swap(i-1, i, node))
    if col+1 < N:  # right
        l.append(swap(i+1, i, node))
    return l


def lis(lst):
    if not lst:
        return []
    memo = [[i] for i in lst]
    for i in range(1, len(lst)):
        for j in range(0, i):
            if lst[i] > lst[j] and len(memo[i]) < len(memo[j]) + 1:
                memo[i] = memo[j]+[lst[i]]
    return max(memo, key=len)


def generate_dcts(board):
    for perm in permutations(board, N):
        perm = "".join(perm)
        for ind in range(N):
            r, c = [], []
            for i in perm:
                if tdct[i][0] == ind and i != ".":
                    r.append(i)
                if tdct[i][1] == ind and i != ".":
                    c.append(i)
            r_dct[(perm, ind)] = len(r)-len(lis(r))
            c_dct[(perm, ind)] = len(c)-len(lis(c))


def total_board_conflicts(board):
    conflicts = 0
    for i in range(N):
        conflicts += r_dct[(board[i * N:i * N + N], i)] + \
            c_dct[("".join(board[c + i] for c in range(0, N ** 2, N)), i)]
    return conflicts


def taxiInc(bi, bf):
    i = bi.index(".")
    row, col = i//N, i % N
    i2 = bf.index(".")
    row2, col2 = i2//N, i2 % N
    letter = bi[i2]
    if row2 != row:
        proper = tdct[letter][0]
        return 1 if abs(proper-row2) < abs(proper-row) else -1
    if col2 != col:
        proper = tdct[letter][1]
        return 1 if abs(proper-col2) < abs(proper-col) else -1



def bi_astar(snode): # 4x4 goal_node
    goal_node = "ABCDEFGHIJKLMNO."
    s_fringe, e_fringe, s_visit, e_visit = [], [], {snode: 0}, {goal_node: 0}
    heappush(s_fringe, (s_taxi:=taxi(snode), snode, 0))
    heappush(e_fringe, (0, goal_node, 0))
    taxiStore[snode], taxiStore[goal_node]= s_taxi, 0
    while s_fringe and e_fringe:
        s_t, s_state, s_d = heappop(s_fringe)
        e_t, e_state, e_d = heappop(e_fringe)

        for c in children(s_state):
            if c not in s_visit:
                s_visit[c] = s_d+1
                newtax = taxiStore[s_state] + taxiInc(s_state, c)
                taxiStore[c] = newtax
                heappush(s_fringe, (s_d+1+newtax+2*total_board_conflicts(c), c, s_visit[c]))
            if c in e_visit:
                return s_d+e_visit[c]
        for c in children(e_state):
            if c not in e_visit:
                e_visit[c] = e_d+1
                newtax = taxiStore[e_state] + taxiInc(e_state, c)
                taxiStore[c] = newtax
                heappush(e_fringe, (e_d+1+newtax+2*total_board_conflicts(c), c, e_visit[c]))
            if c in s_visit:
                return e_d+s_visit[c]
    return None



def astar(snode):
    closed, fringe, node = set(), [], (temptax := taxi(snode), snode, 0)
    taxiStore[snode] = temptax
    heappush(fringe, node)
    while fringe:
        t, state, steps = heappop(fringe)
        # if goal_korf(state):
        if goal(state):
            return steps
        if state not in closed:
            closed.add(state)
            for childState in children(state):
                if childState not in closed:
                    newtax = taxiStore[state] + taxiInc(state, childState)
                    taxiStore[childState] = newtax
                    temp = (steps+1+newtax+2*total_board_conflicts(childState), childState, steps+1)
                    heappush(fringe, temp)
    return None


def astar_bucket(snode):
    closed, open, node = set(), [], (temptax := taxi(snode), snode, 0)
    taxiStore[snode] = temptax
    open = [[] for _ in range(65)]
    open[0].append(node)
    i=0
    while open:
        while not open[i]:
            i+=1
        t, state, steps = open[i].pop()
        if goal(state):
            return steps
        if state not in closed:
            closed.add(state)
            for childState in children(state):
                if childState not in closed:
                    newtax = taxiStore[state] + taxiInc(state, childState)
                    taxiStore[childState] = newtax
                    manhattan = steps+1+newtax+2*total_board_conflicts(childState)
                    temp = (manhattan, childState, steps+1)
                    open[manhattan].append(temp)
    return None


fn = sys.argv[1]
# fn = "4x4_puzzles.txt"
# fn = "5x5_puzzles.txt"
# fn = "korf100.txt"
with open(fn) as f:
    global tdct, N, r_dct, c_dct, taxiStore
    snode = "ABCDEFGHIJKLMNO."
    # snode = "ABCDEFGHIJKLMNOPQRSTUVWX."  # 5x5
    # snode = ".ABCDEFGHIJKLMNO" # korf
    N, r_dct, c_dct = int(len(snode)**0.5), {}, {}
    tdct = {val: (ind//N, ind % N) for ind, val in enumerate(snode)}
    generate_dcts(snode)
    sstart = perf_counter()
    for ind, val in enumerate(f):
        taxiStore = {}
        b = val.strip()
        if parity(b):
            start = perf_counter()
            print(f"Line {ind}: {b}, A* - {astar_bucket(b)} moves in {perf_counter()-start} seconds")
            # print(f"Line {ind}: {b}, A* - {astar(b)} moves in {perf_counter()-start} seconds")
        else:
            print(f"Line {ind}: {b}, A* - no solution found in {perf_counter()-start} seconds")
    print("Total time:", perf_counter()-sstart)
