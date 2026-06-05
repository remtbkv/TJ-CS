def gcd_helper(x, y, f):
    if x%f==0 and y%f==0:
        return f
    else:
        return gcd_helper(x, y, f-1)

def gcd(x, y):
    if x > y:
        f=x
        return gcd_helper(x, y, f)
    elif x < y:
        f=y
        return gcd_helper(x, y, f)

def gcd_euclid(x, y):
    if x%y==0:
        return y
    elif y%x==0:
        return x
    elif x > y:
        return gcd_euclid(x%y, y)
    elif y > x:
        return gcd_euclid(x, y%x)

def lcm(x, y):
    return x*y//gcd_euclid(x, y)

def lcm_n(n):
    if n==1:
        return 1
    return lcm(n, lcm_n(n-1))

import sys
x = int(sys.argv[1])
y = int(sys.argv[2])
n = int(sys.argv[3])
print(gcd(x, y))
print(gcd_euclid(x, y))
print(lcm(x, y))
print(lcm_n(n))