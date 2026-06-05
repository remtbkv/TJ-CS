def grid_moves(n, m):
    if n==0 and m==0:
        return 1
    elif n!=0 and m!=0:
        return grid_moves(n-1, m) + grid_moves(n, m-1)
    elif n!=0 and m==0:
        return grid_moves(n-1, m)
    elif n==0 and m!=0:
        return grid_moves(n, m-1)

def lattice_moves(n, m, x):
    if n==0 and m==0 and x==0:
        return 1
    elif n!=0 and m!=0 and x!=0:
        return lattice_moves(n-1, m, x) + lattice_moves(n, m-1, x) + lattice_moves(n, m, x-1)
    elif n==0 and m!=0 and x!=0:
        return grid_moves(x, m)
    elif n!=0 and m==0 and x!=0:
        return grid_moves(n, x)
    elif n!=0 and m!=0 and x==0:
        return grid_moves(n, m)

def grid_moves_point(n, m, x, y):
    return grid_moves(x, y)*grid_moves(n-x, m-y)

import sys
n = int(sys.argv[1])
m = int(sys.argv[2])
x = int(sys.argv[3])
y = int(sys.argv[4])
print(grid_moves(n, m))
print(lattice_moves(n, m, x))
print(grid_moves_point(n, m, x, y))