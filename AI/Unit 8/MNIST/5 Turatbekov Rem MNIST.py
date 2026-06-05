import pickle, random
import numpy as np
from scipy.ndimage import rotate


store_file = "store_info"
learn = 0.05
epochs = 100
epochs = 6 # genAI

def dump_info(*info):
    with open(store_file, 'wb') as f:
        pickle.dump(info, f)

def load_info():
    with open(store_file, 'rb') as f:
        return pickle.load(f)

def make_pickles(t="train"):
    tset, data, pickle_file = [], f"mnist_{t}.csv", f"pickle_{t}"
    with open(data) as f:
        for l in f:
            l = list(map(int, l.strip().split(",")))
            x, y = np.array([list(map(lambda x: x/255, l[1:]))]).reshape(784, 1), np.array([0 if i != l[0] else 1 for i in range(10)]).reshape(10, 1),
            tset.append((x, y))
    with open(pickle_file, "wb") as f:
        pickle.dump(tset, f)

def load_train():
    with open("pickle_train", "rb") as f:
        return pickle.load(f)


def load_test():
    with open("pickle_test", "rb") as f:
        return pickle.load(f)

def p_net(A_vec, w, b, x):
    a, N = {0: x}, len(network)-1
    for layer in range(1, N+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[N]

# def A(dot_N_F): # new activation function from Unit 9 GenAI
#     temp = np.exp(dot_N_F)
#     return temp/np.sum(temp)


# def Adx(x):  # new from GenAI
#     return 1/np.cosh(x)**2

def A(x):
    return 1/(1+np.exp(-x))

def Adx(x):
    return A(x)*(1-A(x))


a_vec = np.vectorize(A)
adx_vec = np.vectorize(Adx)


def back_prop(data, weights, biases, start=0, learn=learn, A_vec=a_vec, Adx_vec=adx_vec, epochs=epochs):
    w, b = [None]+[i.copy() for i in weights[1:]], [None]+[i.copy() for i in biases[1:]]
    for e in range(start, epochs):
        train = jitter(data) # distortion
        # train = data # normal
        a, dot, delta, N = {}, {}, {}, len(network)-1
        for x, y in train:
            a[0] = x
            for l in range(1, N+1):
                dot[l] = w[l]@a[l-1] + b[l]
                a[l] = A_vec(dot[l])
            delta[N] = (np.eye(y.shape[0]) + (-1 * a[N])) @ y # Gen AI
            # delta[N] = Adx_vec(dot[N])*(y-a[N])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(1, N+1):
                b[l] += learn*delta[l]
                w[l] += (learn*delta[l]) * a[l-1].T
        dump_info(w,b,e)
        m = sum(1 for x, y in test_data if np.argmax(p_net(A_vec, w, b, x)) != np.argmax(y))
        print("Epoch:", e)
        print("Misclassified:", m)
        print(f"Percent wrong: {m/len(test_data)*100}%", )
    return w, b

# updated from GenAI
def fill_network(network):
    weights, biases = [None], [None]
    for i in range(1, len(network)):
        rows = network[i]
        temp_w, temp_b = (rows*network[i-1] + network[i-1])/2, (rows + 1)/2
        r_w, r_b = (3/temp_w)**0.5, (3/temp_b)**0.5
        weights.append(2*r_w*np.random.rand(rows, network[i-1])-r_w)
        biases.append(2*r_b*np.random.rand(rows, 1)-r_b)
    return weights, biases

def jitter(train):
    data = []
    for x, y in train:
        n, row, t  = random.randint(0, 6), np.zeros((1,28)), x.reshape(28,28)
        match n:
            case 1: # shift up
                t = np.vstack((t[1:, :], row))
            case 2: # shift down
                t = np.vstack((row, t[:-1, :]))
            case 3: # shift left
                t = np.hstack((t[:, 1:], row.T))
            case 4: # shift right
                t = np.hstack((row.T, t[:, :-1]))
            case 5: # rotate left 15 deg
                t = rotate(t, angle=15, reshape=False)
            case 6: # rotate right 15 deg
                t = rotate(t, angle=-15, reshape=False)
        data.append((t.reshape((784, 1)), y))
    return data

network = [784, 300, 100, 10]
test_data = load_test()
try:
    w, b, e = load_info()
except:
    w, b = fill_network(network)
    e = 0 

# w, b = fill_network(network) # gen AI fresh start
# e = 0
data = load_train()

back_prop(data, w, b, start=e)