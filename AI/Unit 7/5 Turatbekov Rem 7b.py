import sys
import math
from collections import defaultdict


fn = sys.argv[1]

VARS, data = {}, []
with open(fn) as f:
    for i, l in enumerate(f):
        t = l.strip().split(",")
        if i == 0:
            for ind, v in enumerate(t[:-1]):
                VARS[v] = ind
        else:
            data.append(t)


def entropy(data):
    size, counts = len(data), defaultdict(int)
    for obs in data:
        counts[obs[-1]] += 1
    return -sum((prob := times/size)*math.log(prob, 2) for times in counts.values())

def smaller_data(data, var_index):
    possibles = {}
    for i in data:
        if (var:=i[var_index]) in possibles:
            possibles[var].append(i)
        else:
            possibles[var] = [i]
    return possibles.values()

def entropy_gain(data, var_index):
    return entropy(data) - sum([entropy(v)*len(v)/len(data) for v in smaller_data(data, var_index)])

def make_tree(tree, data, n=0):
    best_var, children, space = max(VARS.keys(), key=lambda c: entropy_gain(data, VARS[c])), {}, " "*n+"*  "
    I = VARS[best_var]
    tree[space+best_var+"?"] = children
    for tdata in smaller_data(data, I):
        for val in sorted(set([obs[I] for obs in tdata])):
            key = " "*(n+2)+"*  "+val
            if entropy(tdata) == 0:
                children[key] = tdata[0][-1]
            else:
                next = children[key] = {}
                make_tree(next, tdata, n+4)

tree = {}
make_tree(tree, data)


def printer(tree):
    for k, v in tree.items():
        if type(v) == dict:
            print(k)
            printer(v)
        else:
            print(k+" --> "+v)

    
def saver(tree, out):
    for k, v in tree.items():
        if type(v) == dict:
            out.append(k+"\n")
            saver(v, out)
        else:
            out.append(k+" --> "+v+"\n")
out = []
saver(tree, out)
with open("treeout.txt", "w") as f:
    f.write("".join(out))
# printer(tree)


def make_tree_display(tree, data, n=0):
    best_var, children, space = max(
        VARS.keys(), key=lambda c: entropy_gain(data, VARS[c])), {}, " "*n+"*  "
    I = VARS[best_var]
    tree[space+best_var +
         "? (entropy gain: "+str(entropy_gain(data, I))+")"] = children
    for tdata in smaller_data(data, I):
        if n == 8:
            print(entropy_gain(tdata, VARS["cap-color"]))
        for val in sorted(set([obs[I] for obs in tdata])):
            key = " "*(n+2)+"*  "+val
            if (e := entropy(tdata)) == 0:
                children[key] = tdata[0][-1]
            else:
                next = children[key+" (current entropy: "+str(e)+")"] = {}
                make_tree_display(next, tdata, n+4)
