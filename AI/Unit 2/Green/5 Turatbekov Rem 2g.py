from time import perf_counter
import random

def goal(state):
    return state.count(None)==0

def get_next_unassigned_var(state):
    l=[]
    for i, v in enumerate(state):
        if v is None:
            l.append(i)
    return random.choice(l) if l else None 

def get_sorted_values(state, var):
    l=[]
    for tc in range(len(state)):
        if tc not in state:
            conflict = False
            for r,c in enumerate(state):
                if c is not None and abs(tc-c)==abs(r-var):
                    conflict = True
                    break
            if not conflict:
                l.append(tc)
    random.shuffle(l)
    return l

def csp_backtracking(state):
    if goal(state):
        return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_values(state, var):
        ns = state.copy()
        ns[var] = val
        result = csp_backtracking(ns)
        if result is not None:
            return result
    return None

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
    for compare in range(var + 1, len(state)):
        left -= 1
        right += 1
        if state[compare] == middle:
            print(var, "middle", compare)
            return False
        if left >= 0 and state[compare] == left:
            print(var, "left", compare)
            return False
        if right < len(state) and state[compare] == right:
            print(var, "right", compare)
            return False
    return True

def raw_conflicts(state, row):
    l = []
    for col in range(len(state)):
        n = state.count(col)
        for r, c in enumerate(state):
            if c!=None and abs(row-r)==abs(col-c):
                n+=1
        l.append(n)
    return l

def generate_ok_board(size):
    l=[None for i in range(size)]
    for r in range(size):
        tmp = raw_conflicts(l,r)
        l[r] = tmp.index(min(tmp))
    return l

def conflicts_for_each_row(state): # real conflicts
    l=[]
    for row, col in enumerate(state):
        n = state.count(col)-1
        for r,c in enumerate(state):
            if r!=row and c is not None and abs(col-c)==abs(row-r):
                n+=1
        l.append(n)
    return l

def conflicts_for_each_col(state, row): # theoretical conflicts
    l=[]
    for col in range(len(state)):
        n = state.count(col)-1
        for r,c in enumerate(state):
            if r!=row and c is not None and abs(col-c)==abs(row-r):
                n+=1
        l.append(n)
    return l

def inc_repair(n):
    state = generate_ok_board(n)
    l = conflicts_for_each_row(state)
    while sum(l):
        w = max(l)
        worst = [i for i,v in enumerate(l) if v==w]
        bad = random.choice(worst)
        conflicts = conflicts_for_each_col(state, bad)
        b = min(conflicts)
        best = [i for i,v in enumerate(conflicts) if v==b]
        good = random.choice(best)
        state[bad] = good

        l = conflicts_for_each_row(state)
        print(sum(l))
        print(state)
    return state

def printBoard(state):
    n = len(state)
    for i in state:
        if i != None:
            print("_ "*i+"Q "+"_ "*(n-i))
        else:
            print("_ "*n)

total = perf_counter()

# for i in range(2):
#     start = perf_counter()
#     board = [None for j in range(30+10*i)]
#     solved = csp_backtracking(board)
#     print(solved)
#     print(perf_counter()-start)
#     print(test_solution(solved))
#     print()

for i in range(2):
    start = perf_counter()
    incsolved = inc_repair(30+5*i)
    # print(incsolved)
    print(perf_counter()-start)
    print(test_solution(incsolved))
    print()

print("Total runtime (sec):",perf_counter()-total)