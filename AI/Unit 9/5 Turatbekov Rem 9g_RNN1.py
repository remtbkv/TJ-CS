import numpy as np
import sys

def ts(n_steps):
    freq1, freq2, offsets1, offsets2 = np.random.rand(4)
    time = np.linspace(0, 1, n_steps)
    series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10))
    series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20))
    series += 0.1 * (np.random.rand(n_steps) - 0.5)
    return series

def trans(test):
    return np.array(test[:-1]).reshape(-1,1), test[-1].reshape((1, 1))


TRAIN = 7000
TEST = 2000


training = [ts(51) for _ in range(TRAIN)]
testing = [ts(51) for _ in range(TEST)]
train_data = [trans(train) for train in training]
test_data = [trans(test) for test in testing]

network = [50, 1]
learn = 0.1
epochs = 100


def N():
    avg = 0
    for test in testing:
        avg += (test[50]-test[49])**2
    print(avg/TEST)


def p_net(A_vec, w, b, x):
    a, N = {0: x}, len(network)-1
    for layer in range(1, N+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[N]


def a_vec(inp):
    return np.tanh(inp)


def adx_vec(inp):
    return 1/np.cosh(inp)**2


def mag(vec):
    return np.sum(np.square(vec)) ** 0.5


def back_prop(data, weights, biases, testing, learn=learn, A_vec=a_vec, Adx_vec=adx_vec, epochs=epochs):
    w, b = [None]+[i.copy() for i in weights[1:]], [None]+[i.copy() for i in biases[1:]]
    for e in range(epochs):
        train = data
        a, dot, delta, N = {}, {}, {}, len(network)-1
        for x, y in train:
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
        avg = 0
        for tx, ty in testing:
            avg += (np.max(ty)-np.max(p_net(A_vec, w, b, tx)))**2
        print(f"Epoch #{e}:",avg/TEST)
    return w, b


def fill_network(network):
    weights, biases = [None], [None]
    for i in range(1,len(network)):
        rows = network[i]
        weights.append(np.random.rand(rows, network[i-1]))
        biases.append(np.random.rand(rows, 1))
    return weights, biases


def D():
    w, b = fill_network(network)
    back_prop(train_data, w, b, test_data)


def fill_RNN_network(network):
    wl, ws, b = [[None] for _ in range(3)]
    for i in range(1,len(network)):
        rows = network[i]
        temp_wl = (rows*network[i-1] + network[i-1])/2
        temp_ws = (rows**2 + rows)/2
        temp_b = (rows + 1)/2
        r_wl = (3/temp_wl)**0.5
        r_ws = (3/temp_ws)**0.5
        r_b = (3/temp_b)**0.5
        wl.append(2*r_wl*np.random.rand(rows, network[i-1])-r_wl)
        ws.append(2*r_ws*np.random.rand(rows, rows)-r_ws)
        b.append(2*r_b*np.random.rand(rows, 1)-r_b)
    return wl, ws, b


def RNN(train, wl, ws, b, learn=learn, A=a_vec, Adx=adx_vec, epochs=epochs):
    F, N = len(train[0][0]), len(network)-1
    for e in range(1,epochs+1):
        for x, y in train:
            a, dot, delta = dict(), dict(), dict()
            for L in range(1, N+1):
                a[(L,0)] = np.zeros((len(ws[L]),1))
            for S in range(1, F+1):
                a[(0,S)] = x[S-1].reshape(-1,1)
                for L in range(1, N+1):
                    dot[(L,S)] = wl[L]@a[(L-1,S)] + ws[L]@a[(L,S-1)] + b[L]
                    a[(L,S)] = A(dot[(L,S)])
            delta[(N,F)] = Adx(dot[(N,F)])*(y-a[(N,F)])
            for S in range(F-1, 0, -1):
                delta[(N,S)] = Adx(dot[(N,S)])*(ws[N].T @ delta[(N,S+1)])
            for L in range(N-1, 0, -1):
                delta[(L,F)] = Adx(dot[(L,F)])*(wl[L+1].T @ delta[(L+1,F)])
            for S in range(F-1, 0, -1):
                for L in range(N-1, 0, -1):
                    delta[(L,S)] = Adx(dot[(L,S)])*(ws[L].T @ delta[(L,S+1)]) + Adx(dot[L,S])*(wl[L+1].T @ delta[(L+1,S)])
            for L in range(1, N+1):
                b[L] += learn*sum(delta[(L,S)] for S in range(1,F+1))
                wl[L] += learn*sum(delta[(L,S)]@a[(L-1,S)].T for S in range(1,F+1))
                ws[L] += learn*sum(delta[(L,S)]@a[(L,S-1)].T for S in range(2,F+1))
        print(f"Epoch #{e} mse:", testRNN(test_data, wl, ws, b))
    return wl, ws, b

def testRNN(test, wl, ws, b):
    se, F, N = [], len(test[0][0]), len(network)-1
    for x, y in test:
        a, dot = dict(), dict()
        for L in range(1, N+1):
            a[(L, 0)] = np.zeros((len(ws[L]), 1))
        for S in range(1, F+1):
            a[(0, S)] = x[S-1].reshape(-1,1)
            for L in range(1, N+1):
                dot[(L, S)] = wl[L]@a[(L-1,S)] + ws[L]@a[(L,S-1)] + b[L]
                a[(L, S)] = a_vec(dot[(L,S)])
        se.append(np.square(y-a[(L,S)]))
    return np.mean(se)


def R():
    global network
    network = [1,1]
    wl_1, ws_1, b_1 = fill_RNN_network(network)
    RNN(train_data, wl_1, ws_1, b_1)


match sys.argv[1]:
    case "N":
        N()
    case "D":
        D()
    case "R":
        R()
