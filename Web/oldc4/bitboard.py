# resources learned from: http://blog.gamesolver.org/solving-connect-four/01-introduction/
from collections import OrderedDict
from time import perf_counter

class LRUCache(OrderedDict):
    # "fixed size tansposition table"
    # removes the least recently used (LRU) key when full
    #   -> stores most recently used keys
    # can make the LRU time bounded (check python docs)
    # source: https://docs.python.org/3/library/collections.html#collections.OrderedDict

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


class Board:
    def __init__(self, **kwargs):
        self.board = kwargs['board'] if 'board' in kwargs else [
            ['.' for _ in range(7)] for _ in range(6)]
        self.height = [len([self.board[r][c] for r in range(5, -1, -1) if self.board[r][c] != "."]) for c in range(7)]
        self.moves = 42-("".join("".join(i) for i in self.board)).count(".")
        self.player = "x" if self.moves % 2 == 0 else "o"
        self.moveorder = [3, 2, 4, 1, 5, 0, 6]
        self.history = []
        self.last_move = 0

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

    def make_move(self, col):
        if col in self.possible_moves():
            self.board[5-self.height[col]][col] = self.player
            self.height[col] += 1
            self.moves += 1
            self.history.append(col)
            self.next_player()

    def undo_move(self):
        col = self.history.pop()
        self.height[col] -= 1
        self.board[5-self.height[col]][col] = "."
        self.moves -= 1

    def win(self, result):
        return True if result is not None and result == 1 and self.player == "x" or result == -1 and self.player == "o" else False

    def possible_moves(self):
        return [col for col in self.moveorder if self.height[col] < 6]

    def has_non_losing_moves(self):  # test this logic
        for col in self.possible_moves():
            b = self.copy()
            b[5-self.height[col]][col] = self.player
            g = self.game_result(gameboard=b)
            if g is None or g is not None and g == 0 or self.win(g):
                return True
        return False

    def can_win_next(self):
        for col in self.possible_moves():
            b = self.copy()
            b[5-self.height[col]][col] = self.player
            g = self.game_result(gameboard=b)
            if self.win(g):
                return True
        return False

    def winning_move(self):
        for col in self.possible_moves():
            b = self.copy()
            b[5-self.height[col]][col] = self.player
            g = self.game_result(gameboard=b)
            if self.win(g):
                return [col]
        return []

    def key(self):  # flattened board as string, make bitboard eventually
        return "".join("".join(i) for i in self.board)

    def num_moves(self):
        return self.moves

    def history(self):
        return self.history

    def next_player(self):
        self.player = "o" if self.player == "x" else "x"

    def copy(self):
        return [self.board[r].copy() for r in range(6)]

    def __repr__(self):
        out = ""
        for row in self.board:
            out += " ".join(row) + "\n"
        return out.strip()


def solve(B):
    TT = LRUCache(pow(2, 56))

    def make_entry(value, UB=False, LB=False):
        return {'val': value, 'UB': UB, 'LB': LB}

    def negamax(alpha, beta):
        # development
        # assert not B.can_win_next()

        alpha_og = alpha

        # if B.num_moves() == 42-2:
        #     return 0

        # if not B.has_non_losing_moves(): # has no losing moves -> will lose on next term
        #     print(B)
        #     return -(42 - B.num_moves())//2

        # minVal, maxVal = -(42-2 - B.num_moves())//2, (42-1 - B.num_moves())//2
        # alpha, beta = max(alpha, minVal), min(beta, maxVal)
        # if alpha >= beta:
        #     return beta

        if B.num_moves() == 42:
            return 0

        if B.can_win_next():
            return (42+1-B.num_moves())//2

        maxVal = (42-1 - B.num_moves())//2
        beta = min(beta, maxVal)
        if alpha >= beta:
            return beta


        if (k := B.key()) in TT:
            entry = TT[k]
            if entry['LB']:
                alpha = max(alpha, entry['val'])
            elif entry['UB']:
                beta = min(beta, entry['val'])
            else:
                return entry['val']
            if alpha >= beta:
                return entry['val']

        # condense negamax  and update storing
        # save upper bound: alpha - MIN_SCORE + 1
        # MIN_SCORE = -42//2 + 3;
        # save lower bound: val + MAX_SCORE - 2*MIN_SCORE + 2
            # doesnt check for val = max(val, -negamax)
        # MAX_SCORE = 43//2 - 3;

        val = -42
        for col in B.possible_moves():
            B.make_move(col) # check to make sure move is valid
            val = max(val, -negamax(-beta, -alpha))
            B.undo_move()
            alpha = max(alpha, val)
            if alpha >= beta:
                break

        if val <= alpha_og:
            TT[B.key()] = make_entry(val, UB=True)
        if val >= beta:
            TT[B.key()] = make_entry(val, LB=True)
        else:
            TT[B.key()] = make_entry(val)

        return val

    # iterative deepening
    minV = -(42 - B.num_moves())//2
    maxV = (42+1 - B.num_moves())//2
    while minV < maxV:
        med = minV + (maxV - minV)//2
        if med <= 0 and minV//2 < med:
            med = minV//2
        elif med >= 0 and maxV//2 > med:
            med = maxV//2
        r = negamax(med, med + 1)
        if r <= med:
            maxV = r
        else:
            minV = r
    return minV

    # return negamax(float('-inf'), float('inf'))


gameboard = [['.', '.', '.', '.', '.', '.', '.'],
             ['x', 'o', '.', '.', '.', '.', '.'],
             ['o', 'o', 'x', 'o', 'x', 'o', 'x'],
             ['o', 'x', 'x', 'x', 'o', 'o', 'x'],
             ['o', 'x', 'o', 'x', 'o', 'x', 'o'],
             ['x', 'o', 'x', 'o', 'x', 'o', 'x']]
gameboard[1] = ["."]*7
gameboard[2] = ["."]*7
gameboard[3] = ["."]*7
# o's turn, result = 4 -> O wins

# x turn

# gameboard = [['.', '.', '.', '.', '.', '.', '.'],
#              ['.', 'x', 'x', 'o', 'o', 'x', 'o'],
#              ['x', 'o', 'o', 'x', 'x', 'x', 'o'],
#              ['o', 'x', 'x', 'x', 'o', 'x', 'o'],
#              ['x', 'o', 'o', 'x', 'x', 'o', 'x'],
#              ['x', 'o', 'o', 'o', 'x', 'o', 'o']]

# gameboard = [["." for _ in range(7)] for _ in range(6)]

def game_result(iterboard):
    board = "?"*9
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


B = Board(board=gameboard)

start = perf_counter()
res = solve(B)
print(perf_counter()-start)
b = str(B)
gb = B.copy()
print(b)
print(b.count("x"), b.count("o"))
print(B.player)
print(B.winning_move())
print(res)

# o will lose in 4 moves