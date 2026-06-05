import sys

directions = [1, -1, -9, 9, -10, 10, -11, 11]

def printBoard(board):
    out = ""
    for i in range(10):
        row = ""
        for j in range(10):
            row += board[10*i+j]
        out += row+'\n'
    print(out)

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
