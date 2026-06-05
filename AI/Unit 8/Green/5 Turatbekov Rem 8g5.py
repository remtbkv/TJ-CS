import sys
import numpy as np

l = 0.1
x, y = 0, 0
epsilon = 1e-8



def A(x, y):
    return 4*x**2 - 3*x + 2*y**2 + 24*y - 20

def Adx(x, y):
    return 8*x - 3*y + 24

def Ady(x, y):
    return 4*(y-5) - 3*x

def gA(point):
    x, y = point
    return np.array([Adx(x,y), Ady(x,y)])


def B(x, y):
    return (1 - y)**2 + (x - y)**2

def Bdx(x,y):
    return 2*(x-y**2)

def Bdy(x,y):
    return 2*(-2*x*y + 2*y**3 + y - 1)

def gB(point):
    x,y = point
    return np.array([Bdx(x,y), Bdy(x,y)])



def magn(vec):
    return np.sum(np.square(vec)) ** 0.5


def main():
    g = gA if sys.argv[1]=="A" else gB
    pos = np.array([x, y], dtype='float64')
    while magn(g(pos)) > epsilon:
        print("Current location:")
        print(pos)
        g_vec = np.array(g(pos))
        print("Current gradient vector:")
        print(g_vec)
        print()
        pos -= l*g_vec
main()