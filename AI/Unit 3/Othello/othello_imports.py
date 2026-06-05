import sys, time


def game_over(board):
    return len(possible_moves(board, "x"))+len(possible_moves(board, "o")) == 0

def possible_moves(board, token):
    moves, directions = [], [1, -1, -9, 9, -10, 10, -11, 11]
    ot = "xo".replace(token,"")
    for ind, val in enumerate(board):
        if val==".":
            for dir in directions:
                cur = ind+dir
                if board[cur]==ot:
                    while board[cur]==ot:
                        cur+=dir
                    if board[cur]==token:
                        moves.append(ind)
    return list(set(moves))

def make_move(board, token, index):
    flip, directions = [], [1, -1, -9, 9, -10, 10, -11, 11]
    ot = "xo".replace(token, "")
    for dir in directions:
        cur = index+dir
        if board[cur]==ot:
            flipInd = [index]
            while board[cur]==ot:
                flipInd.append(cur)
                cur += dir
            if board[cur] == token:
                flip.append(flipInd)
    for dirs in flip:
        for i in dirs:
            board = board[:i]+token+board[i+1:]
    return board

def score(board):
    nx, no = board.count("x"), board.count("o")
    if game_over(board):
        if nx > no: 
            return 1e15 + (nx-no)*1e6
        elif no > nx:
            return -1e15 - (no-nx)*1e6
        else:
            return 0
    scoreX, scoreO = 100*len(possible_moves(board, "x")), 100*len(possible_moves(board, "o"))
    corners_dict = {
        11: {12, 21, 22},
        18: {17, 27, 28},
        81: {71, 72, 82},
        88: {87, 78, 77}
    }
    for corner, adjacents in corners_dict.items():
        if board[corner]==".":
            for adj in adjacents:
                if board[adj]=="x":
                    scoreX -= 1e10
                if board[adj]=="o":
                    scoreO -= 1e10
        if nx+no>12:
            if board[corner]=="x":
                scoreX+=1e7
            if board[corner]=="o":
                scoreO+=1e7
        
    middleEdges = [31, 41, 51, 61, 83, 84, 85, 86, 68, 58, 48, 38, 13, 14, 15, 16]
    for i in middleEdges:
        if board[i]=="x":
            scoreX+=100
        elif board[i]=="o":
            scoreO+=100
    
    return scoreX-scoreO


def negamax(board, depth, player, alpha, beta):
    if not depth or game_over(board):
        return score(board)
    opp = "o" if player=="x" else "x"
    val = -float('inf')
    for i in possible_moves(board, player):
        val = max(val, -negamax(make_move(board, player, i), depth-1, opp, -beta, -alpha))
        # ALPHA/BETA PRUNING HERE
        alpha = max(alpha, val)
        if alpha>=beta:
            break
    return val


def negamax(board, depth, player):
    if not depth or game_over(board):
        return score(board)
    opp = "o" if player == "x" else "x"
    val = -float('inf')
    for i in possible_moves(board, player):
        val = max(val, -negamax(make_move(board, player, i), depth-1, opp))
    return val


def find_next_move(board, player, depth):
    opp = "o" if player == "x" else "x"
    # moves = {index: -negamax(make_move(board, player, index), depth-1, opp, -1e20, 1e20) for index in possible_moves(board, player)}
    moves = {index: -negamax(make_move(board, player, index), depth-1, opp) for index in possible_moves(board, player)}
    best = max(moves.values())

    for index, result in moves.items():
        if result == best:
            move = index
            break
    return move

# results = []
# with open("boards_timing.txt") as f:
#     for line in f:
#         board, token = line.strip().split()
#         temp_list = [board, token]
#         print(temp_list)
#         for count in range(1, 7):
#             print("depth", count)
#             start = time.perf_counter()
#             find_next_move(board, token, count)
#             end = time.perf_counter()
#             temp_list.append(str(end - start))
#         print(temp_list)
#         print()
#         results.append(temp_list)
# with open("boards_timing_my_results.csv", "w") as g:
#     for l in results:
#         g.write(", ".join(l) + "\n")

class Strategy():
#    logging = True  # Optional; see below
   uses_10x10_board = True  # If you delete this line, the server will give you a 64-character 8x8 board instead
   uses_10x10_moves = True  # If you delete this line, the server will expect indices on an 8x8 board instead
   def best_strategy(self, board, player, best_move, still_running):
       depth = 1
       for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
           best_move.value = find_next_move(board, player, depth)
           depth += 1


if __name__ == "__main__":
    board = sys.argv[1]
    player = sys.argv[2]
    depth = 1
    for count in range(board.count(".")):  # No need to look more spaces into the future than exist at all
        print(find_next_move(board, player, depth))
        depth += 1