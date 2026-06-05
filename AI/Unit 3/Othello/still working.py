import sys, time

directions = [1, -1, -9, 9, -10, 10, -11, 11]

def game_over(board):
    return board.count(".")==0

def possible_moves(board, token):
    global directions
    moves = []
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

def score(board):
    nx, ny = board.count("x"), board.count("o")
    corners_dict = {
        11: {12, 21, 22},
        18: {17, 27, 28},
        81: {71, 72, 82},
        88: {87, 78, 77}
    }
    scoreX, scoreO = 0, 0
    movesX, movesO = len(possible_moves(board, "x")), len(possible_moves(board, "o"))
    scoreX += movesX*10
    scoreO += movesO*10
    corners = [11, 18, 81, 88]
    for ci in corners:
        directions = [-1, 1, -10, 10]
        if (p := board[ci]) != ".":
            if p == "x":
                scoreX+=1000
            else:
                scoreO+=1000
        for dir in directions:
            if (p := board[ci+dir])=="o":
                scoreX += 1000
            elif p=="x":
                scoreO += 1000
    scoreX += len(possible_moves(board, "x"))*10000
    scoreO += len(possible_moves(board, "o"))*10000
            
    # corners = [11, 18, 81, 88]
    # for ci in corners:
    #     if (p := board[ci]) != ".":
    #         if nx + ny > 30:
    #             if p == "x":
    #                 scoreX+=10000
    #             else:
    #                 scoreO+=10000
    if game_over(board):
        if nx>ny:
            scoreX+= 1e15 + nx*100
        elif ny>nx:
            scoreO+= 1e15 + ny*100
        else:
            scoreX=0
            scoreO=0
    return scoreX-scoreO


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
#             scorereturn -= 30
#         if board[i] == "o":
#             scorereturn += 30
#     for i in middleedges:
#         if str(board[i]) == "x":
#             scorereturn += 1
#         elif str(board[i]) == "o":
#             scorereturn -= 1
#     return scorereturn


def min_step(board, depth):
    if depth == 0 or game_over(board):
        return score(board)
    results = []
    moves = possible_moves(board, "o")
    if not len(moves):
        return max_step(board, depth-1)
    else:
        for ind in moves:
            results.append(max_step(make_move(board, "o", ind), depth-1))
    return min(results)

def max_step(board, depth):
    if depth == 0 or game_over(board):
        return score(board)
    results=[]
    moves = possible_moves(board, "x")
    if not len(moves):
        return min_step(board, depth-1)
    else:
        for ind in moves:
            results.append(min_step(make_move(board, "x", ind), depth-1))
    return max(results)

def find_next_move(board, player, depth):
    if player == "x":
        moves = {index: min_step(make_move(board, "x", index), depth)
                 for index in possible_moves(board, "x")}
        best = max(moves.values())
    else:
        moves = {index: max_step(make_move(board, "o", index), depth)
                 for index in possible_moves(board, "o")}
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
    # No need to look more spaces into the future than exist at all
    for count in range(board.count(".")):
        print(find_next_move(board, player, depth))
        depth += 1
