import sys
sys.setrecursionlimit(9999999)

'''
def fib(n):
    if n<=1:
        return 1
    else:
        return fib(n-2)+fib(n-1)

'''
def fib_helper(n, prev, cur):
    if n == 0:
        return cur
    else:
        return fib_helper(n-1, cur, cur+prev)

def fib(n): 
    return fib_helper(n, 0, 1)

def is_fib_helper(n, f):
    if f==0:
        return False
    elif fib(f)==n:
        return True
    else:
        return is_fib_helper(n, f-1)

def is_fib(n, f=0):
    if fib(f)>n:
        return is_fib_helper(n, f)
    else:
        return is_fib(n,f+1)

def sum_even_fib(n):
    if n==0:
        return 0
    elif is_fib(n) and n%2==0:
        return n+(sum_even_fib(n-1))
    else:
        return sum_even_fib(n-1)

import sys
print(is_fib(int(sys.argv[1])))
print(sum_even_fib(int(sys.argv[2])))