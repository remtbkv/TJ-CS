import sys, ast
import numpy as np


def p_net(A_vec, w, b, x):
    a, n = {0: x},len(x)
    for layer in range(1, n+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[n]


def step(num):
    return 1 if num > 0 else 0

def step_sigmoid(x):
    return 1/(1+np.exp(-x))


step_vec = np.vectorize(step)
step_s_vec = np.vectorize(step_sigmoid)

def xor_network(x):
    l1_weights, l2_weights = np.array([[1, 1], [1, 1]]), np.array([[1, -2]])
    l1_biases, l2_biases = np.array([[-0.5], [-1.5]]), np.array([[-0.5]])
    weights = [None, l1_weights, l2_weights]
    biases = [None, l1_biases, l2_biases]
    inp_vec = np.array([[x[0]], [x[1]]])
    # XOR HAPPENS HERE
    print(p_net(step_vec, weights, biases, inp_vec)[0, 0])


def dia_network(x):
    l1_weights, l2_weights = np.array([[-1, 1], [1, 1], [1, -1], [-1, -1]]), np.array([[-1, -1, -1, -1]])
    l1_biases, l2_biases = np.array([[-1], [-1], [-1], [-1]]), np.array([[0.5]])
    weights = [None, l1_weights, l2_weights]
    biases = [None, l1_biases, l2_biases]
    inp_vec = np.array([[x[0]], [x[1]]])
    n = p_net(step_vec, weights, biases, inp_vec)[0, 0]
    if n:
        print("inside")
    else:
        print("outside")


def circle_network(x):
    l1_weights, l2_weights = np.array([[1, -1], [-1, -1], [-1, 1], [1, 1]]), np.array([[1, 1, 1, 1]])
    l1_biases, l2_biases = np.array([[I], [I], [I], [I]]), np.array([[J]])
    weights = [None, l1_weights, l2_weights]
    biases = [None, l1_biases, l2_biases]
    inp_vec = np.array([[x[0]], [x[1]]])
    n = p_net(step_s_vec, weights, biases, inp_vec)[0, 0]
    return int(n+0.5)


def check(good=0, size=500):
    l = []
    for _ in range(size):
        x = 2*np.random.rand(2)-1
        a = np.sum(np.square(x))**0.5 < 1
        b = circle_network(x)
        if a == b:
            good+=1
        else:
            l.append(x)
    return l, good/size*100

global I, J
I, J = 2.29674, -3.5

match len(sys.argv[1:]):
    case 2: # diamond
        inp = (float(sys.argv[1]), float(sys.argv[2]))
        dia_network(inp)
    case 1: # XOR
        inp = ast.literal_eval(sys.argv[1])
        xor_network(inp)
    case 0: # circle
        mis, accuracy = check()
        print("Misclassified points:")
        for i in mis:
            print(list(i))
        print()
        print("Accuracy:")
        print(accuracy)
        
