import sys

CORNER_VALUE = 500
EDGE_VALUE = 200
MOVE_VALUE = 25
PIECE_VALUE = 5
LATE_GAME_CORNER_VALUE = 30
LATE_GAME_EDGE_VALUE = 25
LATE_GAME_MOVE_VALUE = 10
LATE_GAME_PIECE_VALUE = 250

def possible_moves(game_board, player_token):
    opposite_token = "o" if player_token == "x" else "x"
    available_moves = set()

    for position in range(11, 90):
        if game_board[position] == player_token:
            for direction in [-11, -10, -9, -1, 1, 9, 10, 11]:
                new_move = explore(game_board, opposite_token, position + direction, direction, False)
                if new_move != -1:
                    available_moves.add(new_move)

    available_moves = list(available_moves)
    for priority_position in [11, 18, 81, 88]:
        if priority_position in available_moves:
            available_moves.insert(0, available_moves.pop(available_moves.index(priority_position)))

    return available_moves

def explore(game_board, opposing_token, current_index, move_direction, is_passed=False):
    while True:
        if game_board[current_index] == opposing_token:
            current_index += move_direction
            is_passed = True
            continue
        if game_board[current_index] == ".":
            return current_index if is_passed else -1
        return -1

def make_move(game_board, player_token, move_index):
    game_board = list(game_board)
    if move_index < 0 or move_index > 99 or game_board[move_index] != ".":
        return ''.join(game_board)
    game_board[move_index] = player_token

    for direction in [-11, -10, -9, -1, 1, 9, 10, 11]:
        if game_board[move_index + direction] not in ["o", "x"]:
            continue
        update_index = explore_fill(game_board, player_token, "o" if player_token == "x" else "x",
                                     move_index + direction, direction)
        if update_index != -1:
            for i in range(move_index, update_index, direction):
                game_board[i] = player_token

    return ''.join(game_board)

def explore_fill(game_board, current_token, opposing_token, current_index, path_direction):
    while True:
        if game_board[current_index] == opposing_token:
            current_index += path_direction
            continue
        if game_board[current_index] == current_token:
            return current_index
        return -1

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
        return  1000 + board_state.count('x')
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
        return ((x_corner_count - o_corner_count)*LATE_GAME_CORNER_VALUE + x_edge_count*-LATE_GAME_EDGE_VALUE + o_edge_count*LATE_GAME_EDGE_VALUE + (x_move_count - o_move_count)* LATE_GAME_MOVE_VALUE + piece_difference* LATE_GAME_PIECE_VALUE)

    return ((x_corner_count - o_corner_count)*CORNER_VALUE + x_edge_count*-EDGE_VALUE + o_edge_count*EDGE_VALUE + (x_move_count - o_move_count)*MOVE_VALUE + piece_difference*PIECE_VALUE)

def find_next_move(board_state, current_player, search_depth):
    if current_player == "x":
        x_moves = set(possible_moves(board_state, "x"))

        if len(x_moves) == 1:
            return x_moves.pop()
        best_move = max(x_moves, key=lambda move:
                 (min_step(make_move(board_state, current_player, move), search_depth, float('-inf'), float('inf'))))
        return best_move

    else:
        o_moves = possible_moves(board_state, "o")
        if len(o_moves) == 1:
            return o_moves.pop()
        best_move = min(o_moves, key=lambda move:
                 (max_step(make_move(board_state, current_player, move), search_depth, float('-inf'), float('inf'))))
        return best_move

class Strategy():

   logging = True  # Optional; see below

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

    for count in range(board.count(".")):
        print(find_next_move(board, player, depth))
        depth += 1