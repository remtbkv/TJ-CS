import random
from heapq import heappop, heappush
from uuid import uuid4

POPULATION_SIZE = 100
NUM_CLONES = 10
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
MUTATION_RATE = .2
FITNESS_TRIALS = 5
HEURISTICS = 6

pieceDict = {
    "I": [[(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1), (0, 2), (0, 3)]],
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    "T": [[(0, 0), (1, 0), (2, 0), (1, 1)], [(0, 0), (0, 1), (1, 1), (0, 2)], [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (1, 2)]],
    "S": [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (0, 1), (1, 1), (0, 2)]],
    "Z": [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]],
    "J": [[(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(2, 0), (0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)]],
    "L": [[(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (1, 0), (0, 1), (0, 2)], [(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (0, 2), (1, 2)]]
}


def make_new_game():
    return [[" "]*10 for _ in range(20)], [0 for _ in range(10)]


def topography(orient):
    return [-min([i[1] for i in orient if i[0] == x]) for x in range(max([i[0] for i in orient])+1)]


def clear(board):
    board = [i.copy() for i in board]
    r, rows = 0, 0
    while r<20:
        if board[r].count("#")==10:
            board = board[:r]+board[r+1:]
            board.append([" "]*10)
            rows+=1
        else:
            r+=1
    return board, rows


def flatten(board):
    return "".join(["".join(i) for i in board[::-1]])


def printB(board):
    if type(board) is list:
        board = flatten(board)
    print("=======================")
    for count in range(20):
        print(' '.join(list(("|" + board[count * 10: (count + 1) * 10] + "|"))), " ", 19-count)
    print("=======================")
    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()


def place_piece(board, heights, orient, c):
    board = [i.copy() for i in board]
    heights = heights.copy()
    sc = c-orient[0][0]
    if sc < 0:
        return -1, None, None
    bt, h = topography(orient), heights[sc:sc+max([i[0] for i in orient])+1]
    r = max([v+bt[i] for i, v in enumerate(h)])
    ic, ir = orient[0]
    for cj, rj in orient:
        nr, nc = r+(rj-ir), c+(cj-ic)
        if nr<0 or nc>9 or nc<0:
            return -1, None, None, ""
        elif nr>19:
            return 0, None, None, "GAME OVER"
        board[nr][nc] = "#"
        heights[nc]+=1
    return True, board, heights




blank_board, blank_heights = make_new_game()

def fitness(strategy):
    n = 0
    for _ in range(FITNESS_TRIALS):
        n += play_strat(strategy)
    return n//FITNESS_TRIALS


def play_strat(strategy):
    board, heights = [i.copy() for i in blank_board], blank_heights.copy()
    points, game = 0, True
    while game:
        game, scores, piece = False, {}, random.choice(list(pieceDict.values()))
        for orient in piece:
            for c in range(10):
                status, tboard, theights, ttboard = place_piece(board, heights, orient, c)
                if status == 0:
                    # RETURN GAME OVER AND MAKE CONDITOINAL IN CLEAR
                if status > 0:
                    tboard, rows_cleared = clear(tboard)
                    tpts = [0, 40, 100, 300, 1200][rows_cleared]
                    tscore = heuristic(tboard, theights, strategy, rows_cleared=rows_cleared)
                    scores[tscore] = (tboard, theights, tpts)
                    game = True
        if game:
            board, heights, pts = scores[max(scores.keys())]
            points += pts
    return points


def play_strat_print(strategy):
    board, heights = [i.copy() for i in blank_board], blank_heights.copy()
    points, game = 0, True
    while game:
        print("Current score: ", points)
        printB(board)
        print()
        game, scores, piece = False, {}, random.choice(list(pieceDict.values()))
        for orient in piece:
            for c in range(10):
                status, tboard, theights = place_piece(board, heights, orient, c)
                if status > 0:
                    tboard, rows_cleared = clear(tboard)
                    tpts = [0, 40, 100, 300, 1200][rows_cleared]
                    tscore = heuristic(tboard, theights, strategy, rows_cleared=rows_cleared)
                    scores[tscore] = (tboard, theights, tpts)
                    game = True
        if game:
            board, heights, pts = scores[max(scores.keys())]
            points += pts
    print("Current score: ", points)
    printB(board)
    return points


def can_play(board, heights):
    for p in pieceDict.values():
        for orient in p:
            for c in range(10):
                status, *_ = place_piece(board, heights, orient, c)
                if status > 0:
                    return True
    return False


def heuristic(board, heights, strategy, rows_cleared=0):
    # NEED: if currnet board is game over
    if not can_play(board, heights):
        print('ethan sucks my balls')
        return -1e10

    holes, \
    cols_with_holes, \
    lines_cleared, \
    diff_height, \
    cumulative_height, \
    roughness \
    = strategy
    
    value, h, cwh, cols = 0, 0, 0, [[board[r][c] for r in range(heights[c])] for c in range(10)]
    for col in cols:
        h += col.count(" ")
        if h:
            cwh+=1

    value += holes * h*10
    value += cols_with_holes * cwh
    value += lines_cleared * rows_cleared
    value += diff_height * abs(max(heights)-min(heights))
    value += cumulative_height * sum(heights)
    value += roughness * sum(abs(heights[i]-heights[i+1]) for i in range(9))

    return value


def evaluate_gen(population={}, generation=0):
    # define population
    if not population:
        for _ in range(POPULATION_SIZE):
            population[str(uuid4())] = [random.uniform(-1,1) for _ in range(HEURISTICS)]
    
    scored, ranked, scores, best_score, best_strategy, i = {}, [], 0, -1, [], 0
    for id, strategy in population.items():
        scored[id] = (score := fitness(strategy))
        print(f"Evaluating strategy {i} --> {score}")
        scores += score
        if score > best_score:
            best_strategy, best_score = strategy, score
        heappush(ranked, (-score, id))
        i+=1
    avg_score = scores//POPULATION_SIZE
    print() 

    # clones
    next_gen = {}
    for _ in range(NUM_CLONES):
        next_gen[id := heappop(ranked)[1]] = population[id]

    # tournament selection
    while len(next_gen) < POPULATION_SIZE:
        tourney = random.sample(list(population.keys()), TOURNAMENT_SIZE*2)
        t1, t2, r1_strat, r2_strat = tourney[:TOURNAMENT_SIZE], tourney[TOURNAMENT_SIZE:], [], []
        for id in t1:
            heappush(r1_strat, (-scored[id], population[id]))
        for id in t2:
            heappush(r2_strat, (-scored[id], population[id]))
        while r1_strat:
            score, p1_strat = heappop(r1_strat)
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                break
        while r2_strat:
            score, p2_strat = heappop(r2_strat)
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                break
        indices = random.sample(range(HEURISTICS), random.randrange(1, HEURISTICS))

        # breeding
        new_strat = [p1_strat[i] for i in indices] + [p2_strat[i] for i in [j for j in range(HEURISTICS) if j not in indices]]

        # mutation        
        if random.random() < MUTATION_RATE:
            ind = random.randrange(HEURISTICS)
            val = new_strat[ind]
            val += random.uniform(-0.05, 0.05)
            while val>1 or val<-1:
                val += random.uniform(-0.1, 0.1)
            new_strat[ind] = val

        next_gen[str(uuid4())] = new_strat
    print(f"Generation: {generation}\nAverage Score: {avg_score}\nBest Score: {best_score}\nBest Strategy: {best_strategy}")
    return next_gen, best_strategy

def assignment():
    game = input("(L)oad strategy or create (N)ew one: ").upper()
    population, generation = {}, 0
    if game=="L":
        fn = input("Enter filename (without .txt) ")
        with open(fn+".txt") as f:
            for l in f:
                population[str(uuid4())] = [float(i) for i in l.strip().split(" ")]
    new_gen, best_strategy = evaluate_gen(population=population, generation=generation)

    answer = ""
    while answer != "E":
        answer = input("(S)ave strategies, (W)atch best strategy, (C)ontinue, or (E)nd? ").upper()
        if answer == "S":
            fn = input("Enter filename (without .txt) ")
            with open(fn+".txt", "w") as f:
                f.write("\n".join([" ".join(str(j) for j in i) for i in new_gen.values()]))
        elif answer == "W":
            play_strat_print(best_strategy)
        elif answer == "C":
            new_gen, best_strategy = evaluate_gen(population=new_gen, generation=generation+1)
        elif answer == "E":
            break
        generation+=1

assignment()

def test():
    population, generation = {}, 0
    while generation < 500:
        population, _ = evaluate_gen(population=population, generation=generation)
        generation += 1

# test()