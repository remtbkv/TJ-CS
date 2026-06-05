from collections import OrderedDict
from time import perf_counter

class Board2:
    def __init__(self, **kwargs):
        self.w = 7
        self.h = 6
        self.board = kwargs['board'] if 'board' in kwargs else [
            ['.' for _ in range(7)] for _ in range(6)]
        self.height = [len([self.board[r][c] for r in range(
            5, -1, -1) if self.board[r][c] != "."]) for c in range(7)]
        self.moves = 42-("".join("".join(i) for i in self.board)).count(".")
        self.player = "x" if self.moves % 2 == 0 else "o"
        self.moveorder = [3, 2, 4, 1, 5, 0, 6]
        self.history = []

    def game_result(self, gameboard=None):
        board = "?"*9
        iterboard = gameboard if gameboard else self.board
        for row in iterboard:
            board += "?"+"".join(row)+"?"
        board += "?"*9
        directions = [1, -1, -8, 8, -9, 9, 10, -10]
        for player in "xo":
            for i in range(72):
                for dir in directions:
                    cur, n = i, 0
                    if board[cur] == player:
                        while board[cur] == player and n < 4:
                            cur += dir
                            n += 1
                        if n == 4:
                            return 1 if player == "x" else -1
        if "".join("".join(i) for i in iterboard).count(".") == 0:
            return 0
        return None

        # must be valid move

    def play(self, col):
        self.board[5-self.height[col]][col] = self.player
        self.height[col] += 1
        self.moves += 1
        self.history.append(col)
        self.player = "o" if self.player=="x" else "x"
        # self.next_player()

    def backtrack(self):
        col = self.history.pop()
        self.height[col] -= 1
        self.board[5-self.height[col]][col] = "."
        self.moves -= 1
        self.player = "o" if self.player=="x" else "x"

    def winning_board_state(self):
        result = self.game_result()
        return True if result is not None and result == 1 and self.player == "x" or result == -1 and self.player == "o" else False

    def get_search_order(self):
        return [col for col in self.moveorder if self.height[col] < 6]

    def get_key(self):
        return "".join("".join(i) for i in self.board)

    def get_score(self):
        return (42+1-self.moves)//2

    def next_player(self):
        self.player = "o" if self.player == "x" else "x"

    def copy(self):
        return [[i for i in self.board[r]] for r in range(6)]

    def __repr__(self):
        out = ""
        for row in self.board:
            out += " ".join(row) + "\n"
        return out.strip()

    def better_move_ordering(self):
        order = []
        other = []
        for col in self.get_search_order():
            if (s:=self.move_score(col)):
                order.append((col,s))
            else:
                other.append(col)
        order.sort(key=lambda x: x[1])
        return [i[0] for i in order] + other

    def move_score(self, col):
        self.play(col)
        score = 0
        if self.winning_board_state():
            score = self.get_score()
        self.backtrack()
        return score


class Board:
    ''' class to store and manipulate connect 4 game states '''

    def __init__(self, width=7, height=6):
        self.w = width
        self.h = height
        self.board_state = [0, 0]
        self.col_heights = [(height + 1) * i for i in range(width)]
        self.moves = 0
        self.history = []
        self.node_count = 0
        # self.buffer = self.__get_buffer()
        self.bit_shifts = self.__get_bit_shifts()
        self.base_search_order = self.__get_base_search_order()
        self.move_order = [3, 2, 4, 1, 5, 0, 6]

    def __repr__(self):
        state = []
        for i in range(self.h):                         # row
            row_str = ''
            for j in range(self.w):                     # col
                pos = 1 << (self.h + 1) * j + i
                if self.board_state[0] & pos == pos:
                    row_str += 'x '
                elif self.board_state[1] & pos == pos:
                    row_str += 'o '
                else:
                    row_str += '. '
            state.append(row_str)
        state.reverse()         # inverted orientation more readable
        return '\n'.join(state)

    def get_current_player(self):
        ''' returns current player: 0 or 1 (0 always plays first) '''
        return self.moves & 1

    def get_opponent(self):
        ''' returns opponent to current player: 0 or 1 '''
        return (self.moves + 1) & 1

    def get_search_order(self):
        ''' returns column search order containing playable columns only '''
        col_order = filter(self.can_play, self.base_search_order)
        return sorted(col_order, key=self.__col_sort, reverse=True)

    def get_mask(self):
        ''' returns bitstring of all occupied positions '''
        return self.board_state[0] | self.board_state[1]

    def get_key(self):
        ''' returns unique game state identifier '''
        return self.get_mask() + self.board_state[self.get_current_player()]

    def can_play(self, col):
        ''' returns true if col (zero indexed) is playable '''
        return not self.get_mask() & 1 << (self.h + 1) * col + (self.h - 1)

    def play(self, col):
        player = self.get_current_player()
        move = 1 << self.col_heights[col]
        self.col_heights[col] += 1
        self.board_state[player] |= move
        self.history.append(col)
        self.moves += 1

    def backtrack(self):
        opp = self.get_opponent()
        col = self.history.pop()
        self.col_heights[col] -= 1
        move = 1 << (self.col_heights[col])
        self.board_state[opp] ^= move
        self.moves -= 1

    def winning_board_state(self):
        ''' returns true if last played column creates winning alignment '''
        opp = self.get_opponent()
        for shift in self.bit_shifts:
            test = self.board_state[opp] & (self.board_state[opp] >> shift)
            if test & (test >> 2 * shift):
                return True
        return False

    def get_score(self):
        ''' returns score of complete game (evaluated for winning opponent) '''
        return - (self.w * self.h + 1 - self.moves) // 2

    def __get_bit_shifts(self):
        return [
            1,              # | vertical
            self.h,         # \ diagonal
            self.h + 1,     # - horizontal
            self.h + 2      # / diagonal
        ]

    def __get_base_search_order(self):
        base_search_order = list(range(self.w))
        base_search_order.sort(key=lambda x: abs(self.w // 2 - x))
        return base_search_order

    def __col_sort(self, col):
        player = self.get_current_player()
        move = 1 << self.col_heights[col]
        count = 0
        state = self.board_state[player] | move

        for shift in self.bit_shifts:
            test = state & (state >> shift) & (state >> 2 * shift)
            if test:
                count += bin(test).count('1')

        return count

    def better_move_ordering(self):
        order = []
        other = []
        for col in self.get_search_order():
            if (s:=self.move_score(col)):
                order.append((col,s))
            else:
                other.append(col)
        order.sort(key=lambda x: x[1])
        return [i[0] for i in order] + other
    
    def move_score(self, col):
        self.play(col)
        score = 0
        if self.winning_board_state():
            score = self.get_score()
        self.backtrack()
        return score
    

class LRUCache(OrderedDict):
    # limit size, removing the least recently used key when full
    # source: https://docs.python.org/3/library/collections

    def __init__(self, maxsize=128, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]


# 3453452226667775714


def get_tt_entry(value, UB=False, LB=False):
    return {'value': value, 'UB': UB, 'LB': LB}


def solve(board):
    TT = LRUCache(4096)

    def recurse(alpha, beta):
        alpha_original = alpha

        if board.winning_board_state():
            return board.get_score()
        elif board.moves == 42:
            return 0
        
        minVal = -(42-2 - board.moves)//2
        alpha = max(alpha, minVal)
        if alpha >= beta:
            return beta

        maxVal = (42-1 - board.moves)//2
        beta = min(beta, maxVal)
        if alpha >= beta:
            return beta

        # transposition table lookup
        if board.get_key() in TT:
            entry = TT[board.get_key()]
            if entry['LB']:
                alpha = max(alpha, entry['value'])  # lower bound stored in TT
            elif entry['UB']:
                beta = min(beta, entry['value'])    # upper bound stored in TT
            else:
                return entry['value']               # exact value stored in TT
            if alpha >= beta:
                return entry['value']               # cut-off (from TT)

        # negamax implementation
        value = -board.w * board.h
        for col in board.better_move_ordering(): # improved
            board.play(col)
            value = max(value, -recurse(-beta, -alpha))
            board.backtrack()
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # transposition table storage
        if value <= alpha_original:
            TT[board.get_key()] = get_tt_entry(value, UB=True)
        elif value >= beta:
            TT[board.get_key()] = get_tt_entry(value, LB=True)
        else:
            TT[board.get_key()] = get_tt_entry(value)       # store exact in TT

        return value
    
    minV = -(42 - board.moves)//2
    maxV = (42+1 - board.moves)//2
    while minV < maxV:
        med = minV + (maxV - minV)//2
        if med <= 0 and minV//2 < med:
            med = minV//2
        elif med >= 0 and maxV//2 > med:
            med = maxV//2
        r = recurse(med, med + 1)
        if r <= med:
            maxV = r
        else:
            minV = r
    return minV

    # return recurse(-1e9, 1e9)


b = [['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', 'x', '.', '.', '.', 'o', '.'],
    ['.', 'o', 'o', 'x', 'o', 'x', '.'],
    ['.', 'x', 'x', 'o', 'x', 'o', '.']]

# b = [['.', '.', '.', '.', '.', '.', '.'],
#     ['.', 'x', 'x', 'o', 'o', 'x', 'o'],
#     ['x', 'o', 'o', 'x', 'x', 'x', 'o'],
#     ['o', 'x', 'x', 'x', 'o', 'x', 'o'],
#     ['x', 'o', 'o', 'x', 'x', 'o', 'x'],
#     ['x', 'o', 'o', 'o', 'x', 'o', 'o']]

t = Board()
pos = "12122112545343377"  # 64546676767533425 
pos = "3453452226663" #"3453452226667775714"
pos = "34534522266" # hard (next player wins in 15 moves)
pos = "345345222666" # easy (next player wins in 15 moves)
# pos = ""
for i in pos:
    t.play(int(i)-1)
print(t)
print("xo"[t.get_current_player()])
s = perf_counter()
res = solve(t)
print(perf_counter()-s)
print(res)
print()
print()

# t = Board2(board=b)
# print(t)
# print(t.player)
# s = perf_counter()
# res = solve(t)
# print(perf_counter()-s) # takes 110s
# print(res)  # 12

