import sys

word = "" if len(sys.argv) < 4 else sys.argv[3].lower()
finalWordset, wordset = set(), set()
minLength = int(sys.argv[2])
maxLength = 0
with open(sys.argv[1]) as f:
    for line in f:
        if (entry := line.strip().lower()).isalpha() and (l := len(entry)) >= minLength:
            finalWordset.add(entry)
            for i in range(1, l+1):
                wordset.add(entry[:i])
            if l > maxLength:
                maxLength = l


def game_over(word):
    return word in finalWordset


def possible_moves(word):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    moves = []
    for letter in alpha:
        if (newWord := word+letter) in wordset:
            moves.append(newWord)
    return moves


def negamax(word, player):
    if game_over(word):
        return 100
    return max(-negamax(partWord, 1-player) for partWord in possible_moves(word))

    # maxVal = -100
    # for partWord in possible_moves(word):
    #     maxVal = max(maxVal, -negamax(partWord, 1-player))
    #     if maxVal == 100:
    #         break
    # return maxVal

    # val = -100
    # for partWord in possible_moves(word):
    #     val = max(val, -negamax(partWord, 1-player))
    # return val

# player 0 (first) is max, player 1 (second) is min
wins = []
opp = len(word) % 2
win = 100
for partWord in possible_moves(word):
    letter = partWord[-1]
    if -negamax(partWord, opp) == win:
        wins.append(letter)
print(wins)

#  y y y
# abse__
# m m m
# simulate

# print(wordset)
# word = input("Enter word to start: ").lower()
# maxl = len("castrate")
# minl = 4
# player = len(word)%2
# while (len(word)<maxl):
#     print(f"Possible letters for player {player%2}:")
#     print(", ".join(possible_moves(word)))
#     let = input(f"Choose letter: ").lower()
#     word += let
#     print("\nCurrent word: "+word+"\n")
#     if word=="cook":
#         print(word in wordset)
#     if game_over(word):
#         print(f"Player {(player+1)%2} won")
#         break
#     player+=1
