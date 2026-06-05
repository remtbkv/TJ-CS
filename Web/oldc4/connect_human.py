class Board:
    def __init__(self, **kwargs):
        self.board = kwargs['board'] if 'board' in kwargs else [['.' for _ in range(7)] for _ in range(6)]
        self.height = [len([self.board[r][c] for r in range(5, -1, -1) if self.board[r][c] != "."]) for c in range(7)]
        self.player = "x" if self.moves % 2 == 0 else "o"

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
        self.board[5-self.height[col]][col] = self.player
        self.history.append(col)
        self.height[col] += 1
        self.moves += 1
        self.next_player()

    def possible_moves(self):
        return [col for col in self.moveorder if self.height[col] < 6]

    def get_player(self):
        return self.player

    def next_player(self):
        self.player = "o" if self.player == "x" else "x"
        return self.player

    def __repr__(self):
        out = ""
        for row in self.board:
            out += " ".join(row) + "\n"
        return out.strip()

    def board_visual(self):
        return " ".join(str(i) for i in range(1,8))+"\n"+self.__repr__()

def play(B):
    while B.game_result() is None:
        print(B.board_visual())
        print("Current player:",B.get_player())
        col = int(input("Enter col to play: "))-1
        if col in B.possible_moves():
            B.make_move(col)
        print()
    print(B.board_visual())
    print(f"Game over, {B.next_player().upper()} won!")

B = Board()
play(B)