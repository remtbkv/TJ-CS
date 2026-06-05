import sys
from ast import literal_eval

# n = int(sys.argv[1])
# i_goals = literal_eval(sys.argv[2])
# pits = literal_eval(sys.argv[3])
# n_items = int(sys.argv[4])
# i_items = literal_eval(sys.argv[5])
# warps = literal_eval(sys.argv[6])

n = 4
i_goals = [0]
pits = [1, 5, 9]
n_items = 1
i_items = [3]

def reward(state, items):
    if state in pits:
        return -100
    if state in i_goals:
        if sum(items)<n_items:
            return -1e6
        else:
            return 0
    return -1


def valid_moves(i):
    row, col = i//n, i%n
    possible_moves = []
    if col > 0:
        possible_moves.append(i-1)
    if col < n - 1:
        possible_moves.append(i+1)
    if row > 0:
        possible_moves.append(i-n)
    if row < n - 1:
        possible_moves.append(i+n)
    return possible_moves


def init_q():
    temp = [0]*n**2
    while True:
        grid = temp.copy()
        for i in range(n**2):
            if i not in i_goals:
                possible_rewards = [grid[new] for new in valid_moves(i)]
                grid[i] = reward(i)+max(possible_rewards)
        if grid == temp:
            break
        temp = grid.copy()
    for i in range(n):
        print(grid[i*n:i*n+n])
    # for i in range(n):
    #     print(grid[i:i+n])
                    




init_q()