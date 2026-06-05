import numpy as np
import pickle, sys
import matplotlib.pyplot as plt


def ts(n_steps):
    freq1, freq2, offsets1, offsets2 = np.random.rand(4)
    time = np.linspace(0, 1, n_steps)
    series = 0.5 * np.sin((time - offsets1) * (freq1 * 10 + 10))
    series += 0.2 * np.sin((time - offsets2) * (freq2 * 20 + 20))
    series += 0.1 * (np.random.rand(n_steps) - 0.5)
    return series


def trans(test):
    return test[:-10].reshape(-1, 1), test[-10:].reshape((-1, 1))


TRAIN = 7000
TEST = 2000


training_ = [ts(60) for _ in range(TRAIN)]
testing_ = [ts(60) for _ in range(TEST)]
train_data = [trans(train) for train in training_]
test_data = [trans(test) for test in testing_]


global network, learn, epochs
# network = [1, 6, 1]
network = [50, 10]
learn = 0.005
epochs = 50


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


def DNN(train, weights, biases, learn=0.00001, A_vec=a_vec, Adx_vec=adx_vec, epochs=epochs):
    w, b = [None]+[i.copy() for i in weights[1:]], [None]+[i.copy() for i in biases[1:]]
    for ep in range(epochs):
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
        print(f"Epoch #{ep}:", testDNN(w, b))
    return w, b


def testDNN(w, b):
    se = []
    for x, y in test_data:
        e = []
        for ty in y:
            e.append((np.max(ty)-np.max(p_net(a_vec, w, b, x)))**2)
        se.append(np.mean(e)/10)
    return np.mean(se)


def fill_DNN(network):
    weights, biases = [None], [None]
    for i in range(1,len(network)):
        rows = network[i]
        temp_w, temp_b = (rows*network[i-1] + network[i-1])/2, (rows + 1)/2
        r_w, r_b = (3/temp_w)**0.5, (3/temp_b)**0.5
        weights.append(2*r_w*np.random.rand(rows, network[i-1])-r_w)
        biases.append(2*r_b*np.random.rand(rows, 1)-r_b)
    return weights, biases


def fill_RNN(network):
    wl, ws, b = [[None] for _ in range(3)]
    for i in range(1, len(network)):
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


def clip(inp, l=1):
    return np.piecewise(inp, [inp < -l, inp > l, abs(inp) <= l], [lambda x: -l, lambda x: l, lambda x: x])


def RNN_S(train, wl, ws, b, learn=learn, A=a_vec, Adx=adx_vec, epochs=epochs):
    F, N = len(train[0][0]), len(network)-1
    for e in range(1, epochs+1):
        for x, y in train:
            x, y = x[:50], y[0]
            a, dot, delta = dict(), dict(), dict()
            for L in range(1, N+1):
                a[(L, 0)] = np.zeros((len(ws[L]), 1))
            for S in range(1, F+1):
                a[(0, S)] = x[S-1].reshape(1, 1)
                for L in range(1, N+1):
                    dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
                    a[(L, S)] = A(dot[(L, S)])
            delta[(N, F)] = Adx(dot[(N, F)])*(y-a[(N, F)])
            for S in range(F-1, 0, -1):
                delta[(N, S)] = Adx(dot[(N, S)])*(ws[N].T @ delta[(N, S+1)])
            for L in range(N-1, 0, -1):
                delta[(L, F)] = Adx(dot[(L, F)])*(wl[L+1].T @ delta[(L+1, F)])
            for S in range(F-1, 0, -1):
                for L in range(N-1, 0, -1):
                    delta[(L, S)] = Adx(dot[(L, S)])*(ws[L].T @ delta[(L, S+1)]) + Adx(dot[L, S])*(wl[L+1].T @ delta[(L+1, S)])
            for L in range(1, N+1):
                b[L] += learn*sum(clip(delta[(L, S)]) for S in range(1, F+1))
                wl[L] += learn*sum(clip(delta[(L, S)])@a[(L-1, S)].T for S in range(1, F+1))
                ws[L] += learn*sum(clip(delta[(L, S)])@a[(L, S-1)].T for S in range(2, F+1))
        print(f"Epoch {e}:", testRNN_S(wl, ws, b))
    return wl, ws, b


def testRNN_S(wl, ws, b):
    network = [1, 6, 1]
    se = []
    for x, y in test_data:
        out = []
        for _ in range(10):
            x = np.vstack((x, np.array(out).reshape(-1, 1)))
            F, N = len(x), len(network)-1
            a, dot = dict(), dict()
            for L in range(1, N+1):
                a[(L, 0)] = np.zeros((len(ws[L]), 1))
            for S in range(1, F+1):
                a[(0, S)] = x[S-1].reshape(-1, 1)
                for L in range(1, N+1):
                    dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
                    a[(L, S)] = a_vec(dot[(L, S)])
            out.append(a[(L,S)])
        se.append(np.mean(np.square(np.array(out).reshape(-1, 1)-y)))
    return np.mean(se)


def RNN_A(train, wl, ws, b, learn=0.00005, A=a_vec, Adx=adx_vec, epochs=epochs):
    F, N = len(train[0][0]), len(network)-1
    for e in range(1, epochs+1):
        for x, y in train:
            a, dot, delta = dict(), dict(), dict()
            for L in range(1, N+1):
                a[(L, 0)] = np.zeros((len(ws[L]), 1))
            for S in range(1, F+1):
                a[(0, S)] = x[S-1].reshape(-1, 1)
                for L in range(1, N+1):
                    dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
                    a[(L, S)] = A(dot[(L, S)])
            delta[(N, F)] = Adx(dot[(N, F)])*(y-a[(N, F)])
            for S in range(F-1, 0, -1):
                delta[(N, S)] = Adx(dot[(N, S)])*(ws[N].T @ delta[(N, S+1)])
            for L in range(N-1, 0, -1):
                delta[(L, F)] = Adx(dot[(L, F)])*(wl[L+1].T @ delta[(L+1, F)])
            for S in range(F-1, 0, -1):
                for L in range(N-1, 0, -1):
                    delta[(L, S)] = Adx(dot[(L, S)])*(ws[L].T @ delta[(L, S+1)]) + Adx(dot[L, S])*(wl[L+1].T @ delta[(L+1, S)])
            for L in range(1, N+1):
                b[L] += learn*sum(clip(delta[(L, S)]) for S in range(1, F+1))
                wl[L] += learn * sum(clip(delta[(L, S)])@a[(L-1, S)].T for S in range(1, F+1))
                ws[L] += learn * sum(clip(delta[(L, S)])@a[(L, S-1)].T for S in range(2, F+1))
        if e%10==0:
            print(f"Epoch #{e} mse:", testRNN(wl, ws, b))
    return wl, ws, b


def testRNN(wl, ws, b):
    se, F, N = [], len(test_data[0][0]), len(network)-1
    for x, y in test_data:
        a, dot = dict(), dict()
        for L in range(1, N+1):
            a[(L, 0)] = np.zeros((len(ws[L]), 1))
        for S in range(1, F+1):
            a[(0, S)] = x[S-1].reshape(-1, 1)
            for L in range(1, N+1):
                dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
                a[(L, S)] = a_vec(dot[(L, S)])
        se.append(np.square(y-a[(L, S)]))
    return np.mean(se)




def naive():
    return


def D():
    global network, learn
    learn = 0.00001
    network = [50, 10]
    w, b = fill_DNN(network)
    DNN(train_data, w, b)


def R_S():
    global network, learn
    network = [1, 6, 1]
    learn = 0.005
    # learn = 0.00001 -> 0.16
    # 0.001 -> 0.011
    wl_1, ws_1, b_1 = fill_RNN(network)
    RNN_S(train_data, wl_1, ws_1, b_1)


def R_A():
    global network, learn
    # learn = 0.00005
    network = [1, 15, 10]
    wl_1, ws_1, b_1 = fill_RNN(network)
    RNN_A(train_data, wl_1, ws_1, b_1)



def dump(*info, fn="file"):
    with open(fn, 'wb') as f:
        pickle.dump(info, f)


def load(fn):
    with open(fn, 'rb') as f:
        return pickle.load(f)


def graphs():
    fig, axs = plt.subplots(3, 3, figsize=(9, 6))
    p_n, p_d, p_rs, p_ra = [], [], [], []

    # N
    w_d, b_d = load('D')
    wl_rs, ws_rs, b_rs = load('R_S')
    wl_ra, ws_ra, b_ra = load('R_A')

    i = 0
    for x, y in test_data[:9]:
        tx = x
        # N
        p_n = np.full((10,1), x[-1])
        mse_n = np.mean(np.square(y-p_n))

        # D
        network = [50, 10]
        N = len(network)-1
        a = {0: x}
        for layer in range(1, N+1):
            a[layer] = a_vec(w_d[layer] @ a[layer-1] + b_d[layer])
        p_d = a[layer]
        
        # R_S
        x = tx
        network = [1, 6, 1]
        N = len(network)-1
        p_rs = []
        for _ in range(10):
            x = np.vstack((x, np.array(p_rs).reshape(-1, 1)))
            F, N = len(x), len(network)-1
            a, dot = dict(), dict()
            for L in range(1, N+1):
                a[(L, 0)] = np.zeros((len(ws_rs[L]), 1))
            for S in range(1, F+1):
                a[(0, S)] = x[S-1].reshape(-1, 1)
                for L in range(1, N+1):
                    dot[(L, S)] = wl_rs[L]@a[(L-1, S)] + ws_rs[L]@a[(L, S-1)] + b_rs[L]
                    a[(L, S)] = a_vec(dot[(L, S)])
            p_rs.append(a[(L, S)])
        p_rs = np.array(p_rs).reshape(-1,1)

        x = tx
        network = [1, 15, 10]
        F, N = len(test_data[0][0]), len(network)-1
        a, dot = dict(), dict()
        for L in range(1, N+1):
            a[(L, 0)] = np.zeros((len(ws_ra[L]), 1))
        for S in range(1, F+1):
            a[(0, S)] = x[S-1].reshape(-1, 1)
            for L in range(1, N+1):
                dot[(L, S)] = wl_ra[L]@a[(L-1, S)] + ws_ra[L]@a[(L, S-1)] + b_ra[L]
                a[(L, S)] = a_vec(dot[(L, S)])
        p_ra = a[(L, S)]

        mse_d = np.mean(np.square(y-p_d))
        mse_rs = np.mean(np.square(y-p_rs))
        mse_ra = np.mean(np.square(y-p_ra))
        x = tx
        col, row = i%3, i//3
        ax = axs[col, row]
        ax.plot(np.vstack((x,y)), color='black')

        ax.plot(range(50,60), p_n, color='red')
        ax.plot(range(50,60), p_d, color='orange')
        ax.plot(range(50,60), p_rs, color='yellow')
        ax.plot(range(50,60), p_ra, color='green')
        ax.set_title(f'Graph #{i+1}')
        ax.set_xlim(0,60)
        ax.set_ylim(-1,1)
        print(f"MSE of graph #{i+1}:\nNaive - red: {mse_n}\nDNN - orange: {mse_d}\nRNN (step) - yellow: {mse_rs}\nRNN (all) - green: {mse_ra}")
        print()
        i += 1
    plt.tight_layout()
    plt.show()

if len(sys.argv)>1:
    match sys.argv[1]:
        case "N":
            print("do this")
        case "D":
            network, learn = [50, 10], 0.00001
            w1, b1 = fill_DNN(network)
            w, b = DNN(train_data, w1, b1, epochs=100)
            dump(w, b, fn="D")
        case "S":
            network, learn = [1, 6, 1], 0.005
            wl_1, ws_1, b_1 = fill_RNN(network)
            wl, ws, b = RNN_S(train_data, wl_1, ws_1, b_1, epochs=20)
            dump(wl, ws, b, fn="R_S")
        case "A":
            network, learn = [1, 15, 10], 0.009
            try:
                wl_1, ws_1, b_1 = load("R_A")
                # 50 epochs
                # 300 epochs
                # 300 epochs
                # 1000 epochs - 0.013
            except:
                wl_1, ws_1, b_1 = fill_RNN(network)
            wl, ws, b = RNN_A(train_data, wl_1, ws_1, b_1, epochs=1000)
            dump(wl, ws, b, fn="R_A")
else:
    graphs()



# DNN - 0.0167 (50 epochs)
# RNN step - 0.00621 (20 epochs)
# RNN all - 0.0403 (50 epochs)