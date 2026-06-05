import sys, ast
from itertools import product

n = int(sys.argv[1])
i_goals = ast.literal_eval(sys.argv[2])
pits = ast.literal_eval(sys.argv[3])
n_items = int(sys.argv[4])
i_items = ast.literal_eval(sys.argv[5])
w = ast.literal_eval(sys.argv[6])

# n = 5
# i_goals = [0]
# pits = [1, 6, 11, 16, 23, 18, 13, 8]
# n_items = 0
# i_items = []
# w = [(5, 24, 0.1)]


warps = dict()
for start, end, prob in w:
    warps[start] = (end, prob)
    

item_configs = [tuple(i) for i in product([False, True], repeat=len(i_items))]


def make_board():
    board = {}
    for i in range(n**2):
        for config in item_configs:
            q_vals = [None]*4 if i in i_goals else [0]*4
            if i < n:
                q_vals[0] = None
            if i >= n**2 - n:
                q_vals[1] = None
            if i % n == 0:
                q_vals[2] = None
            if (i + 1) % n == 0:
                q_vals[3] = None
            board[(i, tuple(config))] = q_vals
    return board


def update(index, items, dir):
    r = -100 if index in pits else -1
    j = {0: index-n, 1: index+n, 2: index-1, 3: index+1}[dir]
    if index in i_items:
        items = tuple(list(items)[:(ind:=i_items.index(index))]+[True]+list(items)[ind+1:])
    return r, j, items


def reward(next_index, items):
    if next_index in i_goals and sum(items) < n_items:
        return -1e6
    start_q = [q for q in board[(next_index, items)] if q is not None]
    if next_index in warps:
        end, prob = warps[next_index]
        end_q = [q for q in board[(end, items)] if q is not None]
        return (1-prob)*max(start_q, default=0) + prob*max(end_q, default=0)
    else:
        return max(start_q, default=0)


def fill_q(changed=True):
    while changed:
        changed = False
        for index in range(n**2):
            for config in item_configs:
                for direction in range(4):
                    if board[curr := (index, config)][direction] is not None:
                        reward, next_index, items = update(index, config, direction)
                        if board[curr][direction] != (q := reward+reward(next_index, items)):
                            board[curr][direction] = q
                            changed = True


def print_board():
    for r in range(n):
        out = []
        for c in range(n):
            if (q_vals:=board[(r*n+c, tuple([False] * len(i_items)))]) == [None]*4:
                out.append(f'{"x":12}')
            else:
                q = max([q for q in q_vals if q is not None], default=0)
                rounded = f"{q:.0f}" if q == int(q) else f"{q:.3f}"
                out.append(f'{rounded:12}')
        print("".join(out))
                           

board = make_board()
fill_q()
print_board()
