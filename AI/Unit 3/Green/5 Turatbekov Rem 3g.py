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
    dct = dict()
    for i in [ind for ind, val in enumerate(board) if val == "."]:
        dct[i] = board[:i]+player+board[i+1:]
    return dct

def min_step(board):
    if (score := game_over(board)) is not None:
        return score
    results = []
    for next_board in possible_next_boards(board, "O").values():
        results.append(max_step(next_board))
    return min(results)

def max_step(board):
    if (score := game_over(board)) is not None:
        return score
    results = []
    for next_board in possible_next_boards(board, "X").values():
        results.append(min_step(next_board))
    return max(results)

def max_move(board, player):
    moves = {index: [min_step(board), board] for index, board in possible_next_boards(board, player).items()}
    best = max(moves.values())
    for index,result in moves.items():
        if result==best:
            move = index
            break
    return (move, moves)

def min_move(board, player):
    moves = {index: [max_step(board), board] for index, board in possible_next_boards(board, player).items()}
    best = min(moves.values())
    for index, result in moves.items():
        if result == best:
            move = index
            break
    return (move, moves)

def print_board(board):
    print("Current board:")
    print(board[0:3]+"    "+"012")
    print(board[3:6]+"    "+"345")
    print(board[6:9]+"    "+"678")

def play_game(board, ai_x):
    game_end = {"X": {-1: 'loss', 0: 'tie', 1: 'win'}, "O": {-1: 'win', 0: 'tie', 1: 'loss'}}
    x_win, o_win = {"go": max_move, "win": "X"}, {"go": min_move, "win": "O"}
    player_move = {0: x_win, 1: o_win}
    if ai_x==1:
        player_move = {0: o_win, 1: x_win}
    turn = ai_x
    if board.count('.')!=9:
        turn=0
    while (g := game_over(board)) is None:
        win = player_move[turn%2]["win"]
        if turn%2==0:
            player = player_move[turn%2]["go"](board, win)
            for index,result in player[1].items():
                print(f"Moving at {index} results in a {game_end[win][result[0]]}")
            print("\n"+f"I choose space {player[0]}\n")
            board = player[1][player[0]][1]
        else:
            l = [i for i in possible_next_boards(board, win).keys()]
            print(f"You can move to any of these spaces: {', '.join([str(i) for i in l])}.\n")
            ind = int(input("Your choice? "))
            print()
            tmp = list(board)
            tmp[ind] = win
            board = "".join(tmp)
        turn+=1
        print_board(board)
        print()
    if g==0:
        print("We tied!")
    elif ai_x==0 and g==1 or ai_x==1 and g==-1:
        print("I win!")
    else:
        print("You win!")

def play():
    board = sys.argv[1]
    print_board(board)
    print()
    if board.count(".")==9:
        ai_token = input("Should I be X or O? ").upper()
        print()
    elif board.count("X") > board.count("O"):
        ai_token = "O"
    else:
        ai_token = "X"
    play_game(board, ai_x="XO".index(ai_token))
    
play()
