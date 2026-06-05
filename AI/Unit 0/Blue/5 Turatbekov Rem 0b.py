import sys
from heapq import heappush, heappop
from time import perf_counter

start = perf_counter()

f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3]

SET1, SET2, SET3, DICT1, DICT2, HEAP1, HEAP2, HEAP3, lst, z = set(), set(), set(), {}, {}, [], [], [], [], 0
 
with open(f1) as f:
    for l in f:
        n = int(l.strip())
        if n not in SET1:
            heappush(HEAP1, n)
            heappush(HEAP3, n)
        SET1.add(n)
        if n in DICT1:
            DICT1[n]+=1
        else:
            DICT1[n]=1
        if n%53==0:
            z += heappop(HEAP3)

with open(f2) as f:
    for l in f:
        n = int(l.strip())
        if n not in SET2:
            heappush(HEAP2, -n)
        SET2.add(n)
        if n in DICT2:
            DICT2[n]+=1
        else:
            DICT2[n]=1

with open(f3) as f:
    for l in f:
        SET3.add(int(l.strip()))

c=0
for i in SET1:
    if i in SET2:
        c+=1
print("#1:",c)

c=0
for i, v in enumerate(DICT1, start=1):
    if i%100==0 and i>0:
        c+=v
print("#2:",c)

c=0
for i in SET3:
    if i in DICT1:
        c+=DICT1[i]
    if i in DICT2:
        c+=DICT2[i]
print("#3:",c)

print("#4:",[heappop(HEAP1) for i in range(10)])

while len(lst)<10:
    if -HEAP2[0] in DICT2 and DICT2[-HEAP2[0]]>=2:
        lst.append(-heappop(HEAP2))
    else:
        heappop(HEAP2)
print("#5:",lst)

print("#6:",z)


end = perf_counter()
print("Total time:", end - start)
