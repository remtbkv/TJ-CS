import sys
from heapq import heappush, heappop, heapify
from time import perf_counter
from itertools import permutations

# s = sys.argv[1]
# s = "5x5_puzzles.txt"
s = "korf100.txt"

# NMOG .ABC
# KLIE DEFG
# F.BA HIJK
# DHJC LMNO

def taxiConsistent(board):
    d = 0
    for ind, val in enumerate(board):
        if val != ".":
            fr, fc = tdct[val]
            cr, cc = ind//N, ind % N
            d += abs(fr-cr)+abs(fc-cc)
    return d

def parity(n, size):
    count = 0
    for x in range(0, len(n)):
        if n[x] != ".":
            for y in range(x + 1, len(n)):
                if n[y] != "." and n[x] > n[y]:
                    count += 1
    if size % 2 == 1:
        return True if count % 2 == 0 else False
    else:
        ind = "".join(n).index(".")
        nthRow = ind//size
        return True if (nthRow % 2 == 0 and count % 2 == 1) or (nthRow % 2 == 1 and count % 2 == 0) else False

def paritykorf(n, size):
    count = 0
    for x in range(0, len(n)):
        if n[x] != ".":
            for y in range(x + 1, len(n)):
                if n[y] != "." and n[x] > n[y]:
                    count += 1
    if size % 2 == 1:
        return True if count % 2 == 0 else False
    else:
        ind = "".join(n).index(".")
        nthRow = ind//size
        return False if (nthRow % 2 == 0 and count % 2 == 1) or (nthRow % 2 == 1 and count % 2 == 0) else True

def taxicab(n):
    size = int(len(n) ** 0.5)
    alphaCheck = "".join(n).find("A")
    alphaDict = dict()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if alphaCheck != -1:
        for i in range(0, len(n)):
            alphaDict[alpha[i]] = i
    taxiCount = 0
    for i, val in enumerate(n):
        if val != ".":
            desiredInd = alphaDict[alpha[alpha.index(val)]] if alphaCheck != -1 else int(val) - 1
            dy = abs((desiredInd//size) - (i//size))
            dx = abs(i % size - desiredInd % size)
            taxiCount += dy + dx
    return taxiCount

desiredLoc = dict()
taxiDict = dict()

def taxicab_incremental(board1, board2):
    size = int(len(board1) ** 0.5)
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ind2 = board1.index(".")
    ind1 = board2.index(".")
    desiredInd = alpha.index(board2[ind2]) + 1 # FOR KORF
    dy1 = abs((desiredInd//size) - (ind1//size))
    dx1 = abs(ind1 % size - desiredInd % size)
    taxiCount1 = dy1 + dx1
    dy2 = abs((desiredInd//size) - (ind2//size))
    dx2= abs(ind2 % size - desiredInd % size)
    taxiCount2 = dy2 + dx2
    return 1 if taxiCount2 > taxiCount1 else - 1

def taxicabkorf(n):
    size = int(len(n) ** 0.5)
    alphaCheck = "".join(n).find("A")
    alphaDict = dict()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if alphaCheck != -1:
        for i in range(0, len(n)):
            alphaDict[alpha[i]] = i
    taxiCount = 0
    for i, val in enumerate(n):
        if val != ".":
            if alphaCheck != -1:
                desiredInd = alphaDict[alpha[alpha.index(val)]] + 1
            else:
                desiredInd = int(val)
            dy = abs((desiredInd//size) - (i//size))
            dx = abs(i % size - desiredInd % size)
            taxiCount += dy + dx
    return taxiCount

def find_goal_korf(v):
    return v==".ABCDEFGHIJKLMNO"

def find_goal(board):
    indexBlank = board.index(".")
    newBoard = board[0:indexBlank] + board[indexBlank+1:] 
    sortedBoard = sorted(newBoard)
    sortedBoard.append(".")
    return "".join(sortedBoard)

def find_4x4():
    return "ABCDEFGHIJKLMNO."
def find_5x5():
    return "ABCDEFGHIJKLMNOPQRSTUVWX."

def get_children(size, board):
    indexBlank = board.index(".")
    listStates = []
    if indexBlank - size >= 0:
        tempChar = board[indexBlank - size]
        toAdd = list(board)
        toAdd[indexBlank] = tempChar
        toAdd[indexBlank - size] = "."
        listStates.append("".join(toAdd))
    if indexBlank + size <= len(board) - 1:
        tempChar = board[indexBlank + size]
        toAdd = list(board)
        toAdd[indexBlank] = tempChar
        toAdd[indexBlank + size] = "."
        listStates.append("".join(toAdd))
    if indexBlank % size != 0:
        tempChar = board[indexBlank - 1]
        toAdd = list(board)
        toAdd[indexBlank] = tempChar
        toAdd[indexBlank - 1] = "."
        listStates.append("".join(toAdd))
    if (indexBlank + 1) % size != 0:
        tempChar = board[indexBlank + 1]
        toAdd = list(board)
        toAdd[indexBlank] = tempChar
        toAdd[indexBlank + 1] = "."
        listStates.append("".join(toAdd))
    return listStates

def a_starkorf(start):
    closed = set()
    start_node = (taxicabkorf(start), start, 0)
    fringe = list()
    heappush(fringe, start_node)
    while fringe:
        t, v, d = heappop(fringe)
        if find_goal_korf(v) == v:
            return d
        if v not in closed:
            closed.add(v)
            for c in get_children(int(len(start) ** 0.5), v):
                if c not in closed:
                    temp = (d + 1 + taxicabkorf(c), c, d + 1)
                    heappush(fringe, temp)
    return None

def specRowCol(cPerm, desired):#nth row/col, "R" for row, "C" for col, permutation, desired
    conflict = 0
    current = ""
    for i in cPerm:
        if i in desired and i != ".":
            current += i
    fourList = list()
    for i in range(0, len(current)):
        fourDict[i] = 1
        pathDict[i] = list()
        pathDict[i].append(current[i])
    for y in current:
        fourList.append(y)
    lisList = lis(current)
    fourDict.clear()
    pathDict.clear()
    conflict += len(current) - len(lisList)
    return conflict
  
saveDict = dict()
def precalculate(size):
    all =  permutations(find_4x4(), size)##
    size = 4
    desired = ".ABCDEFGHIJKLMNO" # find_goal_korf()#find_5x5()#
    for z in all:
        for i in range(0, size):
            saveDict[(i, "R", "".join(z))] = specRowCol(z, desired[i * size: i * size + size])
        colIndex = [0, 4, 8, 12]
        # colIndex = [0, 5, 10, 15, 20]
        for i in range(0, size):
            desiredCol= ""
            for q in colIndex:
                desiredCol += desired[q + i]
            saveDict[(i, "C", "".join(z))] = specRowCol(z, desiredCol)

# def total_board_conflicts(board):
#     rows = [board[i*N:i*N+N] for i in range(N)]
#     cols = ["".join([board[r*N+c] for r in range(N)]) for c in range(N)]
#     conflicts = 0
#     for ind, r in enumerate(rows):
#         conflicts += r_dct[(r, ind)]
#     for ind, c in enumerate(cols):
#         conflicts += c_dct[(c, ind)]
#     return conflicts


def total_board_conflicts(board):
    conflicts = 0
    for i in range(N):
        conflicts += r_dct[(board[i*N:i*N+N], i)]
        conflicts += c_dct[("".join([board[c+i] for c in range(0,N**2,N)]), i)]
    return conflicts

def taxiInc(bi, bf):
    i = bi.index(".")
    row, col = i//N, i % N
    i2 = bf.index(".")
    row2, col2 = i2//N, i2 % N
    letter = bi[i2]
    if row2 != row:
        proper = tdct[letter][0]
        return 1 if abs(proper-row2) < abs(proper-row) else -1
    if col2 != col:
        proper = tdct[letter][1]
        return 1 if abs(proper-col2) < abs(proper-col) else -1

def a_star(start):
    closed = set()
    size = 4
    ta = taxicabkorf(start)
    taxiDict[start] = ta
    start_node = (ta, start, 0)
    fringe = list()
    heappush(fringe, start_node)
    while fringe:
        t, v, d = heappop(fringe)
        if find_goal_korf(v):
            return d
        if v not in closed:
            closed.add(v)
            for c in get_children(size, v):
                if c not in closed:
                    taxi = taxiDict[v]
                    toAdd = taxicab_incremental(v, c)
                    taxiDict[c] = taxi + toAdd
                    conflicts = 0
                    col = [0, 4, 8, 12]
                    for i in range(0, size):
                        conflicts += saveDict[(i,"R", c[i * size:i * size + size])]
                    for i in range(0, size):
                        colC = ""
                        for u in col:
                            colC += c[u + i]
                        conflicts += saveDict[(i, "C", colC)]
                    temp = (d + 1 + taxi + toAdd + 2 * conflicts, c, d + 1)
                    heappush(fringe, temp)
    return None

fourDict = dict()
pathDict = dict()
def lis(q):
    length = len(q)
    for x in range(0, length):
        for y in range(x, length):
            if q[y] > q[x] and fourDict[y] <= fourDict[x]:
                fourDict[y] = fourDict[x] + 1
                pathDict[y] = list()
                for n in pathDict[x]:
                    pathDict[y].append(n)
                pathDict[y].append(q[y])
    maxi = 0
    longList = list()
    for i in fourDict:
        longList = pathDict[i] if fourDict[i] > maxi else longList
        maxi = len(longList)
    return longList

def row_and_column_conf(n):
    length = len(n)
    size = int(length ** 0.5)
    desired = ".ABCDEFGHIJKLMNO" # FOR KORF
    count = 0
    rowConflicts = 0
    columnConflicts = 0
    while count < length:
        currRow = n[count:count + size]
        desiredRow = desired[count:count + size]
        current = ""
        for i in currRow:
            if i in desiredRow and i != ".":
                current += i
        fourList = list()
        for i in range(0, len(current)):
            fourDict[i] = 1
            pathDict[i] = list()
            pathDict[i].append(current[i])
        for y in current:
            fourList.append(y)
        lisList = lis(current)
        fourDict.clear()
        pathDict.clear()
        rowConflicts += len(current) - len(lisList)
        count += size
    colIndex = [0, 4, 8, 12]
    while colIndex[3] < length:
        current = ""
        currentCol = ""
        for i in colIndex:
            currentCol += n[i] 
        desiredCol = ""
        for i in colIndex:
            desiredCol += desired[i]
        for i in currentCol:
            if i in desiredCol and i != ".":
                current += i
        fourList = list()
        for i in range(0, len(current)):
            fourDict[i] = 1
            pathDict[i] = list()
            pathDict[i].append(current[i])
        for y in current:
            fourList.append(y)
        lisList = lis(current)
        fourDict.clear()
        pathDict.clear()
        columnConflicts += len(current) - len(lisList)
        colIndex = [x + 1 for x in colIndex]
    return 2 * columnConflicts + 2 * rowConflicts

def prestore(n):
    countX = 0
    countY = 0
    size = int(len(n) ** 0.5)
    for i in n:
        desiredLoc[i] = (countX, countY)
        countX += 1
        if countX == size:
            countX = 0
            countY += 1

with open(s) as f:
    lines = [x.strip() for x in f]

precalculate(4)
#print(saveDict)
#print(saveDict[0, "R", "DCBA"])
#prestore("ABCDEFGHIJKLMNO")  



# snode = "ABCDEFGHIJKLMNO."
# snode = "ABCDEFGHIJKLMNOPQRSTUVWX."
snode = ".ABCDEFGHIJKLMNO"
N, r_dct, c_dct, taxiStore = int(len(snode)**0.5), {}, {}, {}
tdct = {val: (ind//N, ind % N) for ind, val in enumerate(snode)}

def _lis3(lst, i, memo):
    if i in memo:
        return memo[i]
    memo[i] = [lst[i]]
    for j in range(i):
        if lst[i] > lst[j]:
            tempLIS = _lis3(lst, j, memo)
            if len(tempLIS)+1 > len(memo[i]):
                memo[i] = tempLIS + [lst[i]]
    return memo[i]

def lis3(lst):
    if not lst:
        return []
    if len(lst)==1:
        return lst
    memo = {}
    return max((_lis3(lst, i, memo) for i in range(1, len(lst))), key=len)

def generate_dcts(board):
    for perm in permutations(board, N):
        perm = "".join(perm)
        for ind in range(N):
            r, c = [], []
            for i in perm:
                if i!=".":
                    if tdct[i][0] == ind:
                        r.append(i)
                    if tdct[i][1] == ind:
                        c.append(i)
            r_dct[(perm, ind)] = len(r)-len(lis3(r))
            c_dct[(perm, ind)] = len(c)-len(lis3(c))



generate_dcts(snode)

count = 0
global bigstart
bigstart = perf_counter()
for i in lines:
    size = int(len(i) ** 0.5)#int(i.split()[0])#
    s = perf_counter() 
    print(i)
    # p = parity(i, size)
    p = paritykorf(i, size)#parity(i, size)#
    if p == True:
       print("Line " + str(count) + ": " + i + ", A* " + str(a_star(i)) + " moves in " + str(perf_counter() - s) +  " seconds")
    else: 
      print("Line " + str(count) + ": " + i + ", no solution, found in " + str(perf_counter() - s) + " seconds")
    # if p == True:
    #     print("Line " + str(count) + ": " + i + ", A* " + str(a_star(i)) + " moves in " + str(perf_counter() - s) +  " seconds")
    # else: 
    #     print("Line " + str(count) + ": " + i + ", no solution, found in " + str(perf_counter() - s) + " seconds")
    #print("Line " + str(count) + ": " + i + ", A* " + str(a_star(i)) + " moves")
    count += 1