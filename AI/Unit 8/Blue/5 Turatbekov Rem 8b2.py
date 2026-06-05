import sys
import numpy as np


def p_net(A_vec, w, b, x):
    a, N = {0: x}, len(x)
    for layer in range(1, N+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[N]

def A(x):
    return 1/(1+np.exp(-x))

def Adx(x):
    return A(x)*(1-A(x))

a_vec = np.vectorize(A)
adx_vec = np.vectorize(Adx)

def mag(vec):
    return np.sum(np.square(vec)) ** 0.5


def error(y, a):
    return 1/2*(mag(y-a)**2)

# challenge 1
# l1_weights, l2_weights = np.array([[1, 1], [-0.5, 0.5]]), np.array([[1, -1], [2, -2]])
# l1_biases, l2_biases = np.array([[1], [-1]]), np.array([[-0.5], [0.5]])
# weights = [None, l1_weights, l2_weights]
# biases = [None, l1_biases, l2_biases]
# weights2 = [None, np.array([[ 1.0000519,   1.00007784], [-0.50494448 , 0.49258328]]), np.array([[ 1.00671011, -0.99746038], [ 2.00189194, -1.99928395]])]
# biases2 = [None, np.array([[1.00002595], [-1.00247224]]), np.array([[-0.49327326], [0.50189663]])]

def back_prop_S(A_vec, Adx_vec, learn, training_set, weights, biases, epochs=1000):
    w, b = [None]+[i.copy() for i in weights[1:]], [None]+[i.copy() for i in biases[1:]]
    for _ in range(epochs):
        a, dot, delta, N = {}, {}, {}, len(training_set[0])
        for x, y in training_set:
            a[0] = x
            for l in range(1, N+1):
                dot[l] = w[l]@a[l-1] + b[l]
                a[l] = A_vec(dot[l])
            delta[N] = Adx_vec(dot[N])*(y-a[N])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(1, N+1):
                b[l] += learn*delta[l]
                w[l] += (learn*delta[l]) * a[l-1].T
            print("Data point:")
            print(x)
            print("Output")
            print(a[2])
            print()
    return w, b

def back_prop_C(A_vec, Adx_vec, learn, training_set, weights, biases, epochs=1000):
    learn1, learn2, learn3, learn4, learn5, learn6 = True, True, True, True, True, True
    w, b = [None]+[i.copy() for i in weights[1:]], [None]+[i.copy() for i in biases[1:]]
    for _ in range(epochs):
        a, dot, delta, N = {}, {}, {}, len(training_set[0])
        for x, y in training_set:
            a[0] = x
            for l in range(1, N+1):
                dot[l] = w[l]@a[l-1] + b[l]
                a[l] = A_vec(dot[l])
            delta[N] = Adx_vec(dot[N])*(y-a[N])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(1, N+1):
                b[l] += learn*delta[l]
                w[l] += (learn*delta[l]) * a[l-1].T
        wrong = sum(1 for x, y in training_set if int(p_net(A_vec, w, b, x).mean() + 0.5) != y)
        if wrong < 200 and learn1:
            learn *= 0.9
            learn1 = False
        if wrong < 150 and learn2:
            learn  *= 0.8
            learn2 = False
        if wrong < 125 and learn3:
            learn *= 0.95
            learn3 = False
        if wrong < 80 and learn4:
            learn *= 0.95
            learn4 = False
        if wrong < 70 and learn5:
            learn *= 0.95
            learn5 = False
        if wrong < 60 and learn6:
            learn *= 0.5
            learn6 = False
        print("Epoch:",_)
        print("Misclassified:",wrong)
        # print(w)
        # print(b)
        print()
    return w, b

def S():
    learn = 10
    weights = [None]+[2*np.random.rand(2, 2)-1 for _ in range(2)]
    biases = [None]+[2*np.random.rand(2, 1)-1 for _ in range(2)]
    t_set = [(np.array([[0], [0]], dtype='float64'), np.array([[0], [0]], dtype='float64')),
            (np.array([[0], [1]], dtype='float64'), np.array([[0], [1]], dtype='float64')),
            (np.array([[1], [0]], dtype='float64'), np.array([[0], [1]], dtype='float64')),
            (np.array([[1], [1]], dtype='float64'), np.array([[1], [0]], dtype='float64'))]
    back_prop_S(a_vec, adx_vec, learn, t_set, weights, biases)

def C():
    learn = 1
    between = 2
    weights = [None, between*np.random.rand(12, 2)-1, between*np.random.rand(4, 12)-1, between*np.random.rand(1, 4)-1]
    biases = [None, between*np.random.rand(12, 1)-1, between*np.random.rand(4, 1)-1, between*np.random.rand(1, 1)-1]
    t_set = []
    for _ in range(10000):
        inp = 3*np.random.rand(2, 1)-1
        t_set.append((inp, np.array([int(np.sum(np.square(inp))**0.5 < 1)])))
    # with open("10000_pairs.txt") as f:
    #     for l in f:
    #         x, y = map(float, l.strip().split())
    #         inp = np.array([[x], [y]], dtype='float64')
    #         t_set.append((inp, np.array([int(np.sum(np.square(inp))**0.5 < 1)])))
    back_prop_C(a_vec, adx_vec, learn, t_set, weights, biases, epochs=1000)

S() if sys.argv[1]=="S" else C()
 