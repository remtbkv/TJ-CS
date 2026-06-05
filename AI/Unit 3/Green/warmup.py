import sys


def game_over(board):
    l = []
    for i in range(3):
        l.append([board[j] for j in range(3*i, 3*i+3)])

    d1row = []
    d2row = []
    xrow = ["X", "X", "X"]
    orow = ["O", "O", "O"]
    for i in range(3):
        d1row.append(l[i][i])
        d2row.append(l[2-i][i])
    if d1row == xrow or d2row == xrow:
        return 1
    elif d1row == orow or d2row == orow:
        return -1

    for c in range(3):
        crow = []
        for r in range(3):
            crow.append(l[r][c])
        if l[c] == xrow or crow == xrow:
            return 1
        elif l[c] == orow or crow == orow:
            return -1
    if (board.count(".") == 0):
        return 0
    return None


def possible_next_boards(board, player):
    l = []
    for i in [ind for ind, val in enumerate(board) if val == "."]:
        l.append(board[:i]+player+board[i+1:])
    return l


games = 0
final_boards = set()
x5 = set()
x7 = set()
x9 = set()
o6 = set()
o7 = set()
o8 = set()
draws = set()


def min_step(board, steps=0):
    global games, final_boards
    if (score := game_over(board)) is not None:
        games += 1
        final_boards.add(board)
        if score == 1 and steps == 5:
            x5.add(board)
        if score == 1 and steps == 7:
            x7.add(board)
        if score == 1 and steps == 9:
            x9.add(board)
        if score == 0:
            draws.add(board)
        return (score, steps)
    results = []
    for next_board in possible_next_boards(board, "O"):
        results.append(max_step(next_board, steps+1))
    return min(results)


def max_step(board, steps=0):
    global games, final_boards
    if (score := game_over(board)) is not None:
        games += 1
        final_boards.add(board)
        if score == -1 and steps == 6:
            o6.add(board)
        if score == -1 and steps == 8:
            o8.add(board)
        if score == 0:
            draws.add(board)
        return (score, steps)
    results = []
    for next_board in possible_next_boards(board, "X"):
        results.append(min_step(next_board, steps+1))
    return max(results)


print(max_step("........."))

print(games, len(final_boards))
print(len(x5), len(x7), len(x9))
print(len(o6), len(o8), len(draws))

# print(max_step("XOOOXOXX."))


def print_board(board):
    print("Current board:")
    print(board[0:3]+"    "+"012")
    print(board[3:6]+"    "+"345")
    print(board[6:9]+"    "+"678")


def play():
    board = sys.argv[1]
    print_board(board)
    player_ai = input("Should I be X or O? ")
    nx = board.count("X")
    ny = board.count("Y")

    if board.count(".") == 9:
        go = input("Human play first or ")
    if nx > ny:
        min_step(board)
    else:
        max_step(board)

# X O O
# O X O
# X X .
