import sys
sys.setrecursionlimit(999999)

N = int(sys.argv[1])
filename = sys.argv[2]

# def candy_prices(money, candy_dct, memo): # recursion limit for last case
#     if money in memo:
#         return memo[money]
#     memo[money] = max(candy_dct[money], max(candy_dct[i] + candy_prices(money-i, candy_dct, memo) for i in range(1, money//2+1)))
#     return memo[money]

def candy_prices(money, candy_dct, memo):
    if money not in memo:
        most = 0
        for i in range(1, money):
            t, c = candy_dct[i], candy_prices(money-1-i, candy_dct, memo)
            most = max(most, t+c)
        memo[money] = most
    return memo[money]


def candy_jar(shelf, i, memo):
    if i in memo:
        return memo[i]
    if i == len(shelf):
        return 0
    if i == len(shelf)-1:
        return max(shelf[i], 0)
    memo[i] = max(candy_jar(shelf, i+1, memo), shelf[i]+candy_jar(shelf,i+1, memo), shelf[i]*shelf[i+1]+candy_jar(shelf, i+2, memo))
    return memo[i]


def lcs(s1, s2, i1, i2, memo):
    if (i1, i2) in memo:
        return memo[(i1, i2)]
    if i1 == len(s1) or i2 == len(s2):
        memo[(i1, i2)] = []
    elif s1[i1] == s2[i2]:
        memo[(i1, i2)] = [s1[i1]] + lcs(s1, s2, i1+1, i2+1, memo)
    else:
        l1 = lcs(s1, s2, i1+1, i2, memo)
        l2 = lcs(s1, s2, i1, i2+1, memo)
        if len(l1) >= len(l2):
            memo[(i1, i2)] = l1
        else:
            memo[(i1, i2)] = l2
    return memo[(i1, i2)]


def _lis(lst, i, memo):
    if i in memo:
        return memo[i]
    memo[i] = [lst[i]]
    for j in range(i):
        if lst[i] > lst[j]:
            tempLIS = _lis(lst, j, memo)
            if len(tempLIS)+1 > len(memo[i]):
                memo[i] = tempLIS + [lst[i]]
    return memo[i]

def lis(lst):
    memo = {}
    return max((_lis(lst, i, memo) for i in range(1, len(lst))), key=len)


def _lds(sl, r, c, num, memo):
    if (r, c) in memo:
        return memo[(r, c)]
    memo[(r, c)] = [num]
    for rp in range(r):
        path_poss = []
        for cp, nump in enumerate(sl[rp]):
            if num < nump:
                tempLIS = _lds(sl, rp, cp, nump, memo)
                if len(tempLIS)+1 > len(memo[(r, c)]) and rp+1 == r:
                    path_poss.append(tempLIS + [num])
                else:
                    break
        memo[(r, c)] = max(path_poss, key=len, default=memo[(r, c)])
    return memo[(r, c)]

def lds(sl):
    memo = {}
    return max((_lds(sl, r, c, num, memo) for r in range(1, len(sl)) for c, num in enumerate(sl[r])), key=len)


def paren(n, max_val_t, min_val_t, max_expr_t, min_expr_t):
    for l in range(2, n+1):
        for begin in range(n-l+1):
            end, max_val, min_val, max_expr, min_expr= begin+l-1, float('-inf'), float('inf'), "", ""
            for op in range(begin,end):
                n1, n2, n3, n4 = max_val_t[begin][op]+max_val_t[op+1][end], min_val_t[begin][op]+min_val_t[op+1][end], max_val_t[begin][op]*max_val_t[op+1][end], min_val_t[begin][op]*min_val_t[op+1][end]
                if n1 > max_val:
                    max_val, max_expr = n1, f"({max_expr_t[begin][op]}) + ({max_expr_t[op+1][end]})"
                if n2 > max_val:
                    max_val, max_expr = n2, f"({min_expr_t[begin][op]}) + ({min_expr_t[op+1][end]})"
                if n3 > max_val:
                    max_val, max_expr = n3, f"({max_expr_t[begin][op]}) * ({max_expr_t[op+1][end]})"
                if n4 > max_val:
                    max_val, max_expr = n4, f"({min_expr_t[begin][op]}) * ({min_expr_t[op+1][end]})"

                if n1 < min_val:
                    min_val, min_expr = n1, f"({max_expr_t[begin][op]}) + ({max_expr_t[op + 1][end]})"
                if n2 < min_val:
                    min_val, min_expr = n2, f"({min_expr_t[begin][op]}) + ({min_expr_t[op + 1][end]})"
                if n3 < min_val:
                    min_val, min_expr = n3, f"({max_expr_t[begin][op]}) * ({max_expr_t[op + 1][end]})"
                if n4 < min_val:
                    min_val, min_expr = n4, f"({min_expr_t[begin][op]}) * ({min_expr_t[op + 1][end]})"

                max_val_t[begin][end], max_expr_t[begin][end], min_val_t[begin][end], min_expr_t[begin][end] = max_val, max_expr, min_val, min_expr
    return max_val_t[0][n-1], max_expr_t[0][n-1]


with open(filename) as f:
    if N == 1:
        for l in f:
            l = [int(i) for i in l.strip().split(" ")]
            candy_dct = dict()
            for price, candy in enumerate(l, start=1):
                candy_dct[price] = candy
            print(candy_prices(len(l), candy_dct, {}))
    elif N == 2:
        for l in f:
            l = [int(i) for i in l.strip().split(" ")]
            print(candy_jar(l, 0, {}))
    elif N == 3:
        for i in f:
            l = i.strip().split()
            l1, l2 = l[0].split(","), l[1].split(",")
            print([int(j) for j in lcs(l1, l2, 0, 0, {})])
    elif N == 4:
        for l in f:
            l = [int(i) for i in l.strip().split(" ")]
            print(lis(l))
    elif N == 5:
        for l in f:
            tl = l.strip().split(" ")
            n, lst = int(tl[0][1:-1]), [int(i) for i in tl[1:]]
            sl = [lst[i*n:i*n+n] for i in range(len(lst)//n)]
            if len(lst) % n != 0:
                sl += [lst[-(len(lst) % n):]]
            print(lds(sl))
    elif N == 6:
        for l in f:
            lst = [int(i) for i in l.strip().split(" ")]
            n = len(lst)

            max_val_t = []
            for _ in range(n):
                max_val_t += [[float('-inf')]*n]
            min_val_t = []
            for _ in range(n):
                min_val_t += [[float('inf')]*n]

            max_expr = []
            for _ in range(n):
                max_expr += [['']*n]
            min_expr = []
            for _ in range(n):
                min_expr += [['']*n]

            for i in range(n):
                max_val_t[i][i], min_val_t[i][i], max_expr[i][i], min_expr[i][i] = lst[i], lst[i], str(lst[i]), str(lst[i])

            out, p = paren(n, max_val_t, min_val_t, max_expr, min_expr)
            print(p, "=",out)