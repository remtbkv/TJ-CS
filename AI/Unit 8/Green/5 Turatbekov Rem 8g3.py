import sys, ast

inp = ast.literal_eval(sys.argv[1])
# inp = (1, 1)


xor_table = [((1,1), 0), ((1,0), 1), ((0,1), 1), ((0, 0), 0)]

def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def perceptron(A, w, b, x):
    return A(dot(w,x) + b)

def step(num):
    return 1 if num>0 else 0

def run_network(x):
    # percep3 - OR
    w13 = 1
    w23 = 1
    w3 = (w13, w23)
    b3 = -0.5

    # percep4 - AND
    w14 = 1
    w24 = 1
    w4 = (w14, w24)
    b4 = -1.5

    # percep5 - negate AND
    w35 = 1
    w45 = -2
    w5 = (w35, w45)
    b5 = -0.5
    # XOR HAPPENS HERE
    n1 = perceptron(step, w3, b3, x)
    n2 = perceptron(step, w4, b4, x)
    print(perceptron(step, w5, b5, (n1, n2)))

run_network(inp)