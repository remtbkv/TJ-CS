gameboard = [['.', '.', '.', '.', '.', '.', '.'],
             ['.', 'x', 'x', 'o', 'o', 'x', 'o'],
             ['x', 'o', 'o', 'x', 'x', 'x', 'o'],
             ['o', 'x', 'x', 'x', 'o', 'x', 'o'],
             ['x', 'o', 'o', 'x', 'x', 'o', 'x'],
             ['x', 'o', 'o', 'o', 'x', 'o', 'o']]

cols = [[gameboard[r][c] for r in range(5, -1, -1) if gameboard[r][c] != "."] for c in range(7)]
cols2 = [len([gameboard[r][c] for r in range(5, -1, -1) if gameboard[r][c] != "."]) for c in range(7)]
def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list

l = ["xxxxxo", "oooxo", "xooxox"]
l2 = ["oooox", "xx"]

moves = 42 - len("".join(flatten(gameboard)).split('.')) + 1
moves2 = 42-("".join("".join(i) for i in gameboard)).count(".")

print(moves, moves2)