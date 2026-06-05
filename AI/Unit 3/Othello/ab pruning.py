import sys, time

directions = [1, -1, -9, 9, -10, 10, -11, 11]

def game_over(board):
    return len(possible_moves(board, "x"))+len(possible_moves(board, "o"))==0

def possible_moves(board, token):
    global directions
    moves = []
    ot = "x" if token=="o" else "o"
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
    global directions
    flip = []
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


# def score(board):
#     xcount = board.count('x')
#     ocount = board.count('o')
#     if game_over(board) == True:
#         if xcount > ocount:
#             return 1000 + xcount - ocount
#         elif xcount < ocount:
#             return -1000 - ocount + xcount
#         else:
#             return 0
#     scorereturn = 0
#     xpossibles = possible_moves(board, "x")
#     opossibles = possible_moves(board, "o")
#     scorereturn = (len(xpossibles) - len(opossibles)) * 20
#     if board.count(".") <= 12:
#         scorereturn += (xcount - ocount)
#     middleedges = [31, 41, 51, 61, 83, 84, 85,
#                    86, 68, 58, 48, 38, 13, 14, 15, 16]
#     corners = [11, 18, 81, 88]
#     cornerneighbors = [12, 21, 22, 17, 27, 28, 71, 72, 82, 87, 77, 78]
#     for i in corners:
#         if str(board[i]) == "x":
#             scorereturn += 150
#         elif str(board[i]) == "o":
#             scorereturn -= 150
#     for i in cornerneighbors:
#         if board[i] == "x":
#             scorereturn -= 300
#         if board[i] == "o":
#             scorereturn += 300
#     for i in middleedges:
#         if str(board[i]) == "x":
#             scorereturn += 1
#         elif str(board[i]) == "o":
#             scorereturn -= 1
#     return scorereturn

CORNER_VALUE = 500
EDGE_VALUE = 200
MOVE_VALUE = 25
PIECE_VALUE = 5
LATE_GAME_CORNER_VALUE = 30
LATE_GAME_EDGE_VALUE = 25
LATE_GAME_MOVE_VALUE = 10
LATE_GAME_PIECE_VALUE = 250


def is_winner(game_board, current_player, opponent):
    if game_board.count(current_player) > game_board.count(opponent) and game_board.count('.') == 0:
        return True
    return False


def max_step(state, depth_level, alpha, beta):
    if depth_level == 0:
        return evaluate_state(state)

    highest_score = float('-inf')

    for possible_move in possible_moves(state, "x"):
        highest_score = max(highest_score, min_step(make_move(state, "x", possible_move), depth_level-1, -beta, -alpha))
        if highest_score >= beta:
            return highest_score
        alpha = max(alpha, highest_score)

    return highest_score


def min_step(state, depth_level, alpha, beta):
    if depth_level == 0:
        return evaluate_state(state)

    lowest_score = float('inf')

    for possible_move in possible_moves(state, "o"):
        lowest_score = min(lowest_score, max_step(make_move(state, "o", possible_move), depth_level-1, -beta, -alpha))
        if lowest_score <= alpha:
            return lowest_score
        beta = min(beta, lowest_score)

    return lowest_score


def evaluate_state(board_state):
    if is_winner(board_state, "x", "o"):
        return 1000 + board_state.count('x')
    if is_winner(board_state, "o", "x"):
        return -1000 - board_state.count('o')

    x_corner_count = 0
    for corner in [11, 18, 81, 88]:
        if board_state[corner] == "x":
            x_corner_count += 1
    o_corner_count = 0
    for corner in [11, 18, 81, 88]:
        if board_state[corner] == "o":
            o_corner_count += 1

    x_edge_count = 0
    for edge in [12, 21, 22, 17, 28, 27, 71, 72, 82, 77, 87, 78]:
        if board_state[edge] == "x":
            x_edge_count += 1
    o_edge_count = 0
    for edge in [12, 21, 22, 17, 28, 27, 71, 72, 82, 77, 87, 78]:
        if board_state[edge] == "x":
            o_edge_count += 1

    x_move_count = len(possible_moves(board_state, "x"))
    o_move_count = len(possible_moves(board_state, "o"))

    piece_difference = board_state.count('x') - board_state.count('o')

    if board_state.count('.') < 20:
        return ((x_corner_count - o_corner_count)*LATE_GAME_CORNER_VALUE + x_edge_count*-LATE_GAME_EDGE_VALUE + o_edge_count*LATE_GAME_EDGE_VALUE + (x_move_count - o_move_count) * LATE_GAME_MOVE_VALUE + piece_difference * LATE_GAME_PIECE_VALUE)

    return ((x_corner_count - o_corner_count)*CORNER_VALUE + x_edge_count*-EDGE_VALUE + o_edge_count*EDGE_VALUE + (x_move_count - o_move_count)*MOVE_VALUE + piece_difference*PIECE_VALUE)


def score(board):
    EDGE = 250
    CORNER = 1000
    MOVE = 25
    PIECE = 5
    L_EDGE = 25
    L_CORNER = 50
    L_MOVE = 5
    L_PIECE = 250

    nx, ny = board.count("x"), board.count("o")
    if game_over(board):
        if nx > ny:
            return 1e9 + nx*100
        elif ny > nx:
            return 1e9 + ny*100
        else:
            return 0
        
    scoreX, scoreO = 0, 0
    
    movesX, movesO = len(possible_moves(board, "x")), len(possible_moves(board, "o"))
    scoreX += movesX*10
    scoreO += movesO*10
    
    middleedges = [31, 41, 51, 61, 83, 84, 85, 86, 68, 58, 48, 38, 13, 14, 15, 16]

    for middle in middleedges:
        if board[middle]=="x":
            scoreX += 1
        elif board[middle]=="o":
            scoreO += 1
    
    corners_dict = {
        11: {12, 21, 22},
        18: {17, 27, 28},
        81: {71, 72, 82},
        88: {87, 78, 77}
    }
    for corner, adjacents in corners_dict.items():
        if board[corner]=="x":
            scoreX += 1000
        elif board[corner]=="o":
            scoreO += 1000
        for adj in adjacents:
            if board[adj]=="x":
                if board[corner]!="x":
                    scoreX -= 100
            elif board[adj]=="o":
                if board[corner]!="o":
                    scoreO -= 100
    
    return scoreX-scoreO


# def max_step(board, depth, alpha, beta):
#     if depth == 0 or game_over(board):
#         # return score(board)
#         return evaluate_state(board)
#     val = float('-inf')
#     for ind in possible_moves(board, "x"):
#         val = max(val, min_step(make_move(board, "x", ind), depth-1, -beta, -alpha))
#         if val>=beta:
#             return val
#         alpha = max(alpha, val)
#     return val


# def min_step(board, depth, alpha, beta):
#     if depth == 0 or game_over(board):
#         # return score(board)
#         return evaluate_state(board)
#     val = float('inf')
#     for ind in possible_moves(board, "o"):
#         val = min(val, min_step(make_move(board, "x", ind), depth-1, -beta, -alpha))
#         if val <= alpha:
#             return val
#         beta = min(beta, val)
#     return val


def find_next_move(board, player, depth):
    if player == "x":
        moves = {index: min_step(make_move(board, "x", index), depth, float('-inf'), float('inf')) for index in possible_moves(board, "x")}
        best = max(moves.values())
    else:
        moves = {index: max_step(make_move(board, "o", index), depth, float('-inf'), float('inf')) for index in possible_moves(board, "o")}
        best = min(moves.values())
    
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
   logging = False  # Optional; see below
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