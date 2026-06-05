import sys, os, random, pickle
import numpy as np

learn = 0.001
epochs = 100
L = 101
text_data = "shakespeare.txt"

def softmax(dot_N_F):
    temp = np.exp(dot_N_F)
    return temp/np.sum(temp)


def softmax_gen(dot_N_F, T=1):
    temp = np.exp(dot_N_F/T)
    return temp/np.sum(temp)


def A_tanh(dot_N_F):
    return np.tanh(dot_N_F)


def Aprime_tanh(dot_N_F):
    return 1/np.cosh(dot_N_F)**2


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


def toHot(text_seq, single=False):
    if single:
        vector = np.zeros((C, 1))
        vector[chars_index[text_seq]][0] = 1
        return vector
    hot_list, L = [], len(chars_index)
    for c in text_seq:
        vector = np.zeros((L, 1))
        vector[chars_index[c]][0] = 1
        hot_list.append(vector)
    return hot_list[:-1], hot_list[-1]


def clip(inp, l=1):
    return np.piecewise(inp, [inp < -l, inp > l, abs(inp) <= l], [lambda x: -l, lambda x: l, lambda x: x])


def RD(wl, ws, b):
    i = 0
    for e in range(epochs):
        for seq in training:
            x, y = toHot(seq)
            a, dot, delta, F = dict(), dict(), dict(), len(x)
            for L in range(1, N+1):
                a[(L, 0)] = np.zeros(b[L].shape)
            for S in range(1, F+1):
                a[(0, S)] = x[S-1]
                for L in range(1, N+1):
                    dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
                    if L==N:
                        a[(L, S)] = softmax(dot[(L, S)])
                    else:
                        a[(L, S)] = A_tanh(dot[(L, S)])
            delta[(N, F)] = (np.eye(y.shape[0]) + (-1 * a[(N, F)])) @ y
            delta[(N-1, F)] = Aprime_tanh(dot[(N-1, F)])*(wl[N].T @ delta[(N, F)])
            for S in range(F-1, 0, -1):
                delta[(N-1, S)] = Aprime_tanh(dot[(N-1, S)])*(ws[N-1].T @ delta[(N-1, S+1)])
            for L in range(N-1, 1, -1):
                delta[(L-1, F)] = Aprime_tanh(dot[(L-1, F)])*(wl[L].T @ delta[(L, F)])
            for S in range(F-1, 0, -1):
                for L in range(N-1, 1, -1):
                    delta[(L-1, S)] = Aprime_tanh(dot[(L-1, S)])*(ws[L-1].T @ delta[(L-1, S+1)]) + Aprime_tanh(dot[L-1, S])*(wl[L].T @ delta[(L, S)])
            for L in range(1, N):
                b[L] += learn*sum(clip(delta[(L, S)]) for S in range(1, F+1))
                wl[L] += learn*sum(clip(delta[(L, S)])@a[(L-1, S)].T for S in range(1, F+1))
                ws[L] += learn*sum(clip(delta[(L, S)])@a[(L, S-1)].T for S in range(2, F+1))
            b[N] += learn*clip(delta[(N,F)])
            wl[N] += learn*clip(delta[(N,F)])@a[(N-1,F)].T
            if i==0:
                print("0")
                print(a[(N,F)])
            if i==10000:
                print("10k")
                print(a[(N,F)])
            if i==100000 == 0:
                print(f"Data {i}")
                dump(wl, ws, b, fn=f"Shakespeare_{i}", loc="output")
            i+=1
    return wl, ws, b


def CCE(wl, ws, b):
    cce = []
    for seq in testing:
        x, y = toHot(seq)
        a, dot, F = dict(), dict(), len(x)
        for L in range(1, N+1):
            a[(L, 0)] = np.zeros((len(ws[L]), 1))
        for S in range(1, F+1):
            a[(0, S)] = x[S-1]
            for L in range(1, N+1):
                dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
                if L == N:
                    a[(L, S)] = softmax(dot[(L, S)])
                else:
                    a[(L, S)] = A_tanh(dot[(L, S)])
        cce.append(-sum(y[ind]*np.log(val) for ind, val in enumerate(a[(N, F)])))
    return np.mean(cce)


def dump(*info, fn="_", loc=""):
    if loc:
        os.makedirs(os.path.join(os.getcwd(), loc), exist_ok=True)
    with open(f"{loc}/{fn}", 'wb') as f:
        pickle.dump(info, f)


def load(fn, loc=""):
    if loc:
        loc+="/"
    with open(f"{loc}{fn}", 'rb') as f:
        return pickle.load(f)


def gen_substrings(text, length):
    return [text[i:i+length] for i in range(len(text)-length+1)]


def setup():
    chars_count, chars_index, text, i = dict(), dict(), "", 0
    with open(text_data) as f:
        for l in f:
            text += (l:=l.lower())
            for c in l:
                chars_count[c] = chars_count[c]+1 if c in chars_count else 1
    for char, _ in sorted(chars_count.items(), key=lambda x: x[1], reverse=True):
        chars_index[char] = i
        i+=1
    subs = list(set(gen_substrings(text, L)))
    random.shuffle(subs)
    portion = int(len(subs)*0.15)
    test_data, train_data = subs[:portion], subs[portion:]
    dump(test_data, fn='testing', loc="data")
    dump(train_data, fn='training', loc="data")
    dump(chars_count, fn='chars_count', loc="data")
    dump(chars_index, fn='chars_index', loc="data")


def load_data():
    training = load("training", loc="data")
    testing = load("testing", loc="data")
    chars_index = load("chars_index", loc="data")
    return training[0], testing[0], chars_index[0]


def gen_text(specs, T=1, length=400):
    wl, ws, b = specs
    chars, F, x = "", length, np.zeros((C, 1))
    a, dot = dict(), dict()
    for L in range(1, N+1):
        a[(L, 0)] = np.zeros(b[L].shape)
    for S in range(1, F+1):
        a[(0, S)] = x
        for L in range(1, N+1):
            dot[(L, S)] = wl[L]@a[(L-1, S)] + ws[L]@a[(L, S-1)] + b[L]
            if L == N:
                a[(L, S)] = softmax_gen(dot[(L, S)], T=T)
            else:
                a[(L, S)] = A_tanh(dot[(L, S)])
        chars += (c := np.random.choice(chars_ordered, p=[i[0] for i in a[(L, S)]]))
        x = toHot(c[-1], single=True)
    print(chars)



training, testing, chars_index = load_data()


chars_ordered = list(chars_index.keys())
C = len(chars_index)
network = [C, 128, 128, C]
N = len(network)-1
if len(sys.argv)>1:
    match sys.argv[1]:
        case "S":
            setup()
        case "T":
            wl, ws, b = fill_RNN(network)
            RD(wl, ws, b)
else:
    n = int(18.9e5)
    gen_text(load(f"Shakespeare_{n}",loc="output"), T=0.675)
