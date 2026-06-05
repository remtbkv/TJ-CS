import sys
from math import log
import random
from heapq import heappop, heappush

ALPHA = "ETAOINSRHLDCUMFPGWYBVKXJQZ" #"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N = 3
POPULATION_SIZE = 500
NUM_CLONES = 1
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 5
MUTATION_RATE = .8

# message = sys.argv[1]

freq = {}
with open("ngrams.txt") as f:
    for l in f:
        s, n = l.strip().split(" ")
        freq[s] = int(n)


def encode(text, cipher):
    return "".join([i if not i.isalpha() else cipher[ALPHA.index(i)] for i in text.upper()])


def decode(text, cipher):
    return "".join([i if not i.isalpha() else ALPHA[cipher.index(i)] for i in text.upper()])


def fitness(n, encoded, cipher):
    f = 0
    decoded = decode(encoded, cipher)
    for i in range(0, len(decoded)-n):
        if (ngram := decoded[i:i+n]) in freq:
            f += log(freq[ngram], 2)
    return f


def climb(text):
    ca = list(ALPHA)
    random.shuffle(ca)
    res = fitness(N, text, ca)
    while True:
        ca2 = ca.copy()
        i, j = random.sample(range(26), 2)
        ca2[i], ca2[j] = ca2[j], ca2[i]
        res2 = fitness(N, text, ca2)
        if res2>res:
            ca, res = ca2, res2
            print(decode(text, ca))
            print()


def create_new_gen(message, population):
    scored = {}
    for cipher in population:
        scored[cipher] = fitness(N, message, cipher)

    ranked = []
    for cipher, score in scored.items():
        heappush(ranked, (-score, cipher))

    next_gen = set()
    for _ in range(NUM_CLONES):
        next_gen.add(heappop(ranked)[1])

    while len(next_gen) < POPULATION_SIZE:
        tmp = random.sample(population, TOURNAMENT_SIZE*2)
        t1, t2, r1, r2 = tmp[:TOURNAMENT_SIZE], tmp[TOURNAMENT_SIZE:], [], []
        for cipher in t1:
            heappush(r1, (-scored[cipher], cipher))
        for cipher in t2:
            heappush(r2, (-scored[cipher], cipher))
        while r1:
            c1 = heappop(r1)[1]
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                break
        while r2:
            c2 = heappop(r2)[1]
            if random.random() < TOURNAMENT_WIN_PROBABILITY:
                break

        cross = random.sample(range(26), CROSSOVER_LOCATIONS)
        new_cipher = ["."]*26
        for i in cross:
            new_cipher[i] = c1[i]
        l = [i for i in range(26) if i not in cross]
        for letter in c2:
            if letter not in new_cipher:
                new_cipher[l.pop(0)] = letter

        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(26), 2)
            new_cipher[i], new_cipher[j] = new_cipher[j], new_cipher[i]
        next_gen.add("".join(new_cipher))
    return next_gen


def solve(message):
    population = set()
    while len(population)<POPULATION_SIZE:
        ca = list(ALPHA)
        random.shuffle(ca)
        population.add("".join(ca))
    population, generations = list(population), 0
    while generations<500:
        next_gen = create_new_gen(message, population)
        population = list(next_gen)
        max_fit, max_cipher = 0, ""
        for cipher in next_gen:
            f = fitness(N, message, cipher)
            if f > max_fit:
                max_fit = f
                max_cipher = cipher
        
        print(f"{generations} {max_fit} {max_cipher} {decode(message,max_cipher)}")
        print()
        generations+=1


solve(message)
