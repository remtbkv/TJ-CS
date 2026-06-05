import sys
from time import perf_counter
from collections import deque

banktxt = sys.argv[1]
puzzlestxt = sys.argv[2]

N = 6 # word length

dctTime, puzzlesTime = perf_counter(), perf_counter()

alpha = "abcdefghijklmnopqrstuvwxyz"

bank = dict()
with open(banktxt) as f:
    for l in f:
        bank[l.strip()] = {}
for word in bank: # slower for small N but faster in long run
    s = set()
    for i in range(N):
        for j in alpha:
            t = word[:i]+j+word[i+1:]
            if t!=word and t in bank:
                s.add(t)
    bank[word]=s
print("Time taken to create dictionary:",perf_counter()-dctTime)
print("There are",len(bank),"words in this dict")

with open(puzzlestxt) as f:
    puzzles = [l.strip() for l in f]

def swap(i1, i2, node):
    a, b = min(i1, i2), max(i1, i2)
    return node[:a] + node[b] + node[a+1:b] + node[a] + node[b+1:]

def children(word):
    return bank[word]

def BFS(word, goal):
    fringe = deque()
    visited = set()
    fringe.append((word, 1, [word]))
    visited.add(word)
    while fringe:
        node, steps, path = fringe.popleft()
        if node==goal:
            return (steps, path)
        for c in children(node):
            if c not in visited:
                tempPath = path.copy()
                tempPath.append(c)
                fringe.append((c, steps+1 , tempPath))
                visited.add(c)
    return None

for i, v in enumerate(puzzles):
    print("Line:",i)
    l = v.split()
    t = BFS(l[0], l[1])
    if t:
        n, path = t
        print("Length:",n)
        print("\n".join(path),"\n")
    else:
        print("No solution!")

print("\nTime to solve all these puzzles:", perf_counter()-puzzlesTime,"\n")

brainTeasersTime = perf_counter()

n1=0
for v in bank.values():
    if len(v)==0:
        n1+=1

s = set()
def BFS_2(word):
    global s
    fringe = deque()
    visited = set()
    fringe.append(word)
    visited.add(word)
    while fringe:
        node = fringe.popleft()
        for c in children(node):
            if c not in visited:
                tempPath = [i for i in path]
                tempPath.append(c)
                fringe.append(c)
                visited.add(c)
                s.add(c)
        if len(fringe)==0:
            return len(visited)

n2, n3=0,0
for i in bank:
    if i not in s:
        n2 = max(n2, BFS_2(i))
        if len(bank[i])>0:
            n3+=1

dct = dict()
vst = set()

def BFS_3(word):
    global dct, vst
    fringe = deque()
    visited = set()
    fringe.append((word, 1, [word]))
    visited.add(word)
    vst.add(word)
    while fringe:
        node, steps, path = fringe.popleft()
        for c in children(node):
            if c not in visited:
                tempPath = [i for i in path]
                tempPath.append(c)
                fringe.append((c, steps+1 , tempPath))
                visited.add(c)
        if len(fringe)==0 and steps>=2:
            dct[word] = path

for i in bank:
    if i not in vst:
        BFS_3(i)

m, p = 0, []
for v in dct.values():
    if len(v)>m:
        p = v
        m = len(v)

print("1) There are ",n1,"singletons")
print("2) The biggest subcomponent has",n2,"words")
print("3) There are",n3,"'clumps' (subgraphs with at least two words)")
print(f"4) The longest path is:, [[{p[0]}, {p[-1]}], {m}]")
print("Length is:",m)
print("The solution to this puzzle is:")
print("\n".join(p))
print("\nTime to solve brainteasers: ",perf_counter()-brainTeasersTime)