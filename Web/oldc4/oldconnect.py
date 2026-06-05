gameboard = "?"*9
for i in range(6):
    gameboard += "?" + "."*7 + "?"
gameboard += "?"*9
turn = 0

def printBoard():
    out = ""
    for i in range(10,63,9):
        out += gameboard[i:i+7] + "\n"
    print(out)

def board():
    out = "1 2 3 4 5 6 7\n"
    for i in range(10,63,9):
        out += " ".join(list(gameboard[i:i+7])) + "\n"
    print(out)

board()

def possible_moves(gameboard):
    moves = []
    for i in range(55, 62):
        cur = i
        while cur>=0 and gameboard[cur] in "xo":
            cur-=9
        if cur>=0:
            moves.append(cur)
    return moves

def game_over(gameboard):
    directions = [1, -1, 8, -9, 9, -9, 10, -10]
    for player in "xo":
        for i in range(72):
            for dir in directions:
                cur, n = i, 0
                if (gameboard[cur]==player):
                    while gameboard[cur]==player and n<4:
                        cur+=dir
                        n+=1
                    if (n==4):
                        return 1 if player=="x" else -1
    return 0 if gameboard.count(".")==0 else None

def make_move(gameboard, ind, player):
    board = list(gameboard)
    board[ind]=player
    return "".join(board)

def negamax(board, depth, player):
    if depth==0 or game_over(board):
        return 100
    opp = "o" if player=="x" else "x"
    val = -100
    for ind in possible_moves(board):
        val = max(val, -negamax(make_move(board, depth-1, ind, player), opp))
        if (val == 100):
            break
    return val

def negamax(board, depth, player, alpha, beta):
    if not depth or game_over(board):
        return 100
    opp = "o" if player == "x" else "x"
    val = -float('inf')
    for i in possible_moves(board, player):
        val = max(val, -negamax(make_move(board, player, i),
                  depth-1, opp, -beta, -alpha))
        # ALPHA/BETA PRUNING HERE
        alpha = max(alpha, val)
        if alpha >= beta:
            break
    return val

wins = []
opp = "o"
win = 100
for ind in possible_moves(gameboard):
    if -negamax(make_move(gameboard, ind, "x"), opp) == win:
        wins.append(ind)
print(wins)
