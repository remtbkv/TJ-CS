from time import perf_counter

start = perf_counter()

def is_prime(x):
    return not [i for i in range(2, int(x**0.5)+1) if x%i==0]

# 1
print("#1:",sum([i for i in range(1000) if i%3==0 or i%5==0]))

# 2
f, x, i, n = [1, 1], 0, 1, 1
def fib(x): 
    if x<len(f):
        return f[x]
    sum = fib(x-2) + fib(x-1)
    f.append(sum)
    return f[x]


while n<4000000:
    n = fib(i)
    if n%2==0:
        x+=n
    i+=1
print("#2:",x)

# 3
N, x = 600851475143, 0
for i in range(int(N**0.5), 1, -1):
    if is_prime(i) and N%i==0:
        x = i
        break
print("#3",x)

# 4
def is_pal(x): # takes str
    return x[::-1]==x
x=1
for i in range(1,1000):
    for j in range(1,1000):
        if is_pal(str(n := i*j)):
            x = max(x, n)
print("#4:",x)

# 5
N, x = 20, 1
def gcd(a, b):
    while b != 0:
        t = b
        b = a%b
        a = t
    return a

for i in range(1,N+1):
    x*=i//gcd(i, x)

print("#5", x)

# 6
N=100
print("#6",sum(i for i in range(1, N+1))**2-sum([i**2 for i in range(1, N+1)]))

# 7
N, x, i = 10001, 1, 0
while i<N:
    x+=1
    if is_prime(x):
        i+=1
print("#7", x)

# 8
s = "731671765313306249192251196744265747423553491949349698352031277450632623957831801698480186947885184385" +\
    "861560789112949495459501737958331952853208805511125406987471585238630507156932909632952274430435576689" +\
    "664895044524452316173185640309871112172238311362229893423380308135336276614282806444486645238749303589" +\
    "072962904915604407723907138105158593079608667017242712188399879790879227492190169972088809377665727333" +\
    "001053367881220235421809751254540594752243525849077116705560136048395864467063244157221553975369781797" +\
    "784617406495514929086256932197846862248283972241375657056057490261407972968652414535100474821663704844" +\
    "031998900088952434506585412275886668811642717147992444292823086346567481391912316282458617866458359124" +\
    "566529476545682848912883142607690042242190226710556263211111093705442175069416589604080719840385096245" +\
    "544436298123098787992724428490918884580156166097919133875499200524063689912560717606058861164671094050" +\
    "7754100225698315520005593572972571636269561882670428252483600823257530420752963450"

N, x = 13, 0
for i in range(0, len(s)-N):
    n = int(s[i])
    for j in range(i+1, i+N):
        n*=int(s[j])
    if n>x:
        x=n
print("#8",x)

# 9
x = 0
for c in range(335,997):
    for b in range(334,1000-c):
        a = 1000-c-b
        if a+b+c==1000 and a**2+b**2==c**2:
            x = a*b*c
print("#9",x)

# 11
data = [[ 8,  2, 22, 97, 38, 15,  0, 40,  0, 75,  4,  5,  7, 78, 52, 12, 50, 77, 91,  8],
       [49, 49, 99, 40, 17, 81, 18, 57, 60, 87, 17, 40, 98, 43, 69, 48,  4, 56, 62,  0],
       [81, 49, 31, 73, 55, 79, 14, 29, 93, 71, 40, 67, 53, 88, 30,  3, 49, 13, 36, 65],
       [52, 70, 95, 23,  4, 60, 11, 42, 69, 24, 68, 56,  1, 32, 56, 71, 37,  2, 36, 91],
       [22, 31, 16, 71, 51, 67, 63, 89, 41, 92, 36, 54, 22, 40, 40, 28, 66, 33, 13, 80],
       [24, 47, 32, 60, 99,  3, 45,  2, 44, 75, 33, 53, 78, 36, 84, 20, 35, 17, 12, 50],
       [32, 98, 81, 28, 64, 23, 67, 10, 26, 38, 40, 67, 59, 54, 70, 66, 18, 38, 64, 70],
       [67, 26, 20, 68,  2, 62, 12, 20, 95, 63, 94, 39, 63,  8, 40, 91, 66, 49, 94, 21],
       [24, 55, 58,  5, 66, 73, 99, 26, 97, 17, 78, 78, 96, 83, 14, 88, 34, 89, 63, 72],
       [21, 36, 23,  9, 75,  0, 76, 44, 20, 45, 35, 14,  0, 61, 33, 97, 34, 31, 33, 95],
       [78, 17, 53, 28, 22, 75, 31, 67, 15, 94,  3, 80,  4, 62, 16, 14,  9, 53, 56, 92],
       [16, 39,  5, 42, 96, 35, 31, 47, 55, 58, 88, 24,  0, 17, 54, 24, 36, 29, 85, 57],
       [86, 56,  0, 48, 35, 71, 89,  7,  5, 44, 44, 37, 44, 60, 21, 58, 51, 54, 17, 58],
       [19, 80, 81, 68,  5, 94, 47, 69, 28, 73, 92, 13, 86, 52, 17, 77,  4, 89, 55, 40],
       [ 4, 52,  8, 83, 97, 35, 99, 16,  7, 97, 57, 32, 16, 26, 26, 79, 33, 27, 98, 66],
       [88, 36, 68, 87, 57, 62, 20, 72,  3, 46, 33, 67, 46, 55, 12, 32, 63, 93, 53, 69],
       [ 4, 42, 16, 73, 38, 25, 39, 11, 24, 94, 72, 18,  8, 46, 29, 32, 40, 62, 76, 36],
       [20, 69, 36, 41, 72, 30, 23, 88, 34, 62, 99, 69, 82, 67, 59, 85, 74,  4, 36, 16],
       [20, 73, 35, 29, 78, 31, 90,  1, 74, 31, 49, 71, 48, 86, 81, 16, 23, 57,  5, 54],
       [ 1, 70, 54, 71, 83, 51, 54, 69, 16, 92, 33, 48, 61, 43, 52,  1, 89, 19, 67, 48]]

N, x, l = 4, 0, len(data)

# horizontal
for row in range(l):
    for col in range(l-N):
        n = 1
        for i in range(N):
            n*=data[row][col+i]
        x=max(x,n)
# vertical
for col in range(l):
    for row in range(l-N):
        n = 1
        for i in range(N):
            n*=data[row+i][col]
        x=max(x,n)

# diagonals

# --> x
for horiz_offset in range(l-N+1):
    for diag in range(l-horiz_offset-N+1):
        n = 1
        for i in range(N):
            n*=data[diag+i][diag+horiz_offset+i]
        x = max(n, x)

# --> y
for vo in range(l-N+1):
    for col in range(l-vo-N+1):
        n=1
        for i in range(N):
            n*=data[vo+col+i][col+i]
        x = max(n, x)

# <-- x 
for col in range(l-1 ,N-2, -1):
    for row in range(col-N+2):
        n=1
        for i in range(N):
            n*=data[row+i][col-row-i]
        x = max(n, x)

# <-- y
for row in range(l-N):
    for col in range(l-1, row+N-1, -1):
        n=1
        for i in range(N):
            n*=data[row+(l-col)+i][col-i]
        x = max(n, x)

print("#11", x)

# 12
def primeFactors(a):
    dct = {}
    if a==2:
        dct[2]=1
    for i in range(2, int(a**0.5)+1):
        while a%i==0:
            a//=i
            if i in dct:
                dct[i]+=1
            else:
                dct[i]=1
    if a>2:
        dct[a]=1
    return dct

N, n, x, f = 500, 0, 0, 0
while f<=N:
    x += 1
    n += x
    f=1
    for i, v in primeFactors(n).items():
        f*=v+1

print("#12",n)

# 14
N, x, c, m = 1000000, 0, 0, 0
for i in range(2, N):
    c, t = 1, i
    while t != 1:
        if t%2==0:
            t//=2
        else:
            t = 3*t+1
        c+=1
    if c>m:
        x = i
        m = c

print("#14",x)
    

# 18
"""
I thought that we were only given the data list formatted in that way to make
the problem easier, where originally the data was given in a stream of ints.
Because of this, I flattened the list to replicate what I thought solving the
"raw" problem would be like (without a nicely formatted matrix). This is why
my code is very convoluted and I realize that if I just use the data matrix
given, I can make the code a lot cleaner, shorter and and more readable
"""

data = [[75],
       [95, 64],
       [17, 47, 82],
       [18, 35, 87, 10],
       [20,  4, 82, 47, 65],
       [19,  1, 23, 75,  3, 34],
       [88,  2, 77, 73,  7, 63, 67],
       [99, 65,  4, 28,  6, 16, 70, 92],
       [41, 41, 26, 56, 83, 40, 80, 70, 33],
       [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
       [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
       [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
       [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
       [63, 66,  4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
       [ 4, 62, 98, 27, 23,  9, 70, 98, 73, 93, 38, 53, 60,  4, 23]]

t = [j for i in data for j in i]
l = int((-1+(1+8*len(t))**0.5)//2)
x, lw, rw = t[0], [j*(j+1)//2 for j in range(0, l)], [j*(j+1)//2-1 for j in range(1, l+1)] # indices for L/R wings

for i in range(1, len(t)):
    if i in lw:
        t[i]+=t[lw[lw.index(i)-1]]
    elif i in rw:
        t[i]+=t[rw[rw.index(i)-1]]
    else:
        j=i
        while j not in lw:
            j-=1
        n = j - lw[lw.index(j)-1] + 1
        t[i]+=max(t[i-n], t[i-n+1])
    x = max(t[i], x)

print("#18:",x)

#24
D, N = "0123456789", 1000000

def fact(x):
    if x==1:
        return 1
    return x*fact(x-1)

def perm(digits, nth):
    if (l := len(digits))==1:
        return digits
    nth %= (n := fact(l))
    ppd = n//l
    return (d := digits[nth//ppd])+perm(digits.replace(d,""), nth)

print("#24",perm(D, N-1))

# 28
N, x, j = 1001, 1, 1
for i in range(1, 1 + N//2):
    for k in range(4):
        j+=i*2
        x+=j

print("#28",x)

print("#29", len(set([a**b for a in range(2,101) for b in range(2,101)])))

end = perf_counter()
print("Total time:", end - start)
