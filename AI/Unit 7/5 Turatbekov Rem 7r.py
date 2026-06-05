import sys, random, math
import matplotlib.pyplot as plt

def entropy(data):
    size, counts = len(data), {}
    for obs in data:
        if (c := obs[-1]) not in counts:
            counts[c] = 0
        counts[c] += 1
    return -sum((prob := times/size)*math.log(prob, 2) for times in counts.values())

def smaller_data(data, var_index):
    possibles = {}
    for i in data:
        if (var := i[var_index]) in possibles:
            possibles[var].append(i)
        else:
            possibles[var] = [i]
    return possibles.values()

def entropy_gain(data, var_index):
    return entropy(data) - sum([entropy(v)*len(v)/len(data) for v in smaller_data(data, var_index)])

def make_tree(tree, data):
    if entropy(data) and all(entropy_gain(data, vi)==0 for vi in range(len(VARS))):
        var = random.choice(list(VARS.keys()))
        tree[var] = {val: random.choice(list(classifications)) for val in VALS[VARS[var]]}
        return
    
    best_var, children = max(VARS.keys(), key=lambda c: entropy_gain(data, VARS[c])), {}
    tree[best_var], I = children, VARS[best_var]

    for tdata in smaller_data(data, I):
        for val in sorted(set([obs[I] for obs in tdata])):
            if entropy(tdata) == 0:
                children[val] = tdata[0][-1]
            else:
                next = children[val] = {}
                make_tree(next, tdata)

def printer(tree):
    for k, v in tree.items():
        if type(v) == dict:
            print(k)
            printer(v)
        else:
            print(k+" --> "+v)

def classify(tree, vector):
    node = tree.copy()
    while type(node) == dict:
        var = next(iter(node))
        val = vector[VARS[var]]
        if val not in node[var]:
            node = node[var][random.choice(list(node[var].keys()))]
        else:
            node = node[var][val]
    return node


fn = sys.argv[1]
test_size, start, end, step = [int(i) for i in sys.argv[2:]]

VARS, VALS, nonmissing, missing, classifications = {}, {}, [], [], set()
with open(fn) as f:
    for i, l in enumerate(f):
        l = l.strip().split(",")
        if not i:
            for ind, v in enumerate(l[:-1]):
                VARS[v] = ind
            continue
        elif "?" not in l:
            nonmissing.append(l)
            classifications.add(l[-1])
            for ind, val in enumerate(l):
                if ind not in VALS:
                    VALS[ind] = set()
                VALS[ind].add(val)
        missing.append(l)


random.shuffle(missing)

test, samples = missing[-test_size:], missing[:-test_size]

majority = {c: {vi: {val: 0 for val in VALS[vi]} for vi in range(len(VARS))} for c in classifications}
for vector in missing:
    for ind, val in enumerate(vector[:-1]):
        if val != "?":
            majority[vector[-1]][ind][val] += 1

filled_missed = []
for l in missing:
    for ind, val in enumerate(l):
        if val == "?":
            l[ind] = max(majority[l[-1]][ind].keys())
    filled_missed.append(l)

filled_test, filled_sample = filled_missed[-test_size:], filled_missed[:-test_size]

accuracy = []
for size in range(start, end, step):
    train = random.sample(filled_sample, size)
    while not entropy(train):
        train = random.sample(filled_sample, size)
    make_tree(tree:={}, train)
    good = sum(1 for c in filled_test if classify(tree, c[:-1]) == c[-1])
    accuracy.append((size, good/test_size*100))


x,y = zip(*accuracy)
plt.scatter(x, y)
plt.xlabel('Size')
plt.ylabel('Accuracy')
plt.show()
