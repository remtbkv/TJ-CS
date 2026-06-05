import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

N_HIDDEN = 20
N_NEURONS = 10
network = [4] + N_HIDDEN*[N_NEURONS] + [3]
learn = 0.01
epochs = 50

data = load_iris()
X, y = data.data, data.target
y = np.eye(3)[y]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train_data = list(zip(X_train, y_train))
test_data = list(zip(X_test, y_test))


def p_net(A_vec, w, b, x):
    a, N = {0: x}, len(network)-1
    for layer in range(1, N+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[N]

def A(x):
    # return np.tanh(x)
    # return np.maximum(0, x)
    return 1/(1+np.exp(-x))

def Adx(x):
    # return 1/np.cosh(x)**2
    # return x>0
    return A(x)*(1-A(x))

a_vec = np.vectorize(A)
adx_vec = np.vectorize(Adx)

def clip(inp, l=1):
    return np.piecewise(inp, [inp < -l, inp > l, abs(inp) <= l], [lambda x: -l, lambda x: l, lambda x: x])

def DNN(w, b, start=0, learn=learn, A_vec=a_vec, Adx_vec=adx_vec, epochs=epochs):
    gradient = {i: [] for i in range(1, N_HIDDEN+1)}
    train_A, test_A = [], []
    outer, inner = [], []
    for e in range(start, epochs):
        a, dot, delta, N = {}, {}, {}, len(network)-1
        print(f"Epoch {e}")
        for x, y in train_data:
            x = np.array(x).reshape(-1, 1, order='F')
            y = np.array(y).reshape(-1, 1, order='F')
            a[0] = x
            for l in range(1, N+1):
                dot[l] = w[l]@a[l-1] + b[l]
                a[l] = A_vec(dot[l])
            delta[N] = Adx_vec(dot[N])*(y-a[N])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(1, N+1):
                b[l] += learn*clip(delta[l])
                w[l] += (learn*clip(delta[l])) * a[l-1].T
                # b[l] += learn*delta[l]
                # w[l] += (learn*delta[l]) * a[l-1].T
        # for l in range(1, N_HIDDEN+1):
        #     print(np.mean(gradient[l]), end = " ")
        # print(input())
        inner.append(np.mean([np.mean(w[1][i]) for i in range(w[1].shape[0])]))
        outer.append(np.mean([np.mean(w[-1][i]) for i in range(w[-1].shape[0])]))
        for l in range(1, N_HIDDEN+1):
            gradient[l].append(np.mean(delta[l]))
        train_correct, test_correct = 0, 0
        for x, y in train_data:
            x = np.array(x).reshape(-1, 1, order='F')
            y = np.array(y).reshape(-1, 1, order='F')
            pred = p_net(a_vec, w, b, x)
            if np.argmax(pred) == np.argmax(y):
                train_correct += 1
        for x, y in test_data:
            x = np.array(x).reshape(-1, 1, order='F')
            y = np.array(y).reshape(-1, 1, order='F')
            pred = p_net(a_vec, w, b, x)
            if np.argmax(pred) == np.argmax(y):
                test_correct += 1
        train_A.append((e, train_correct/len(train_data)))
        test_A.append((e, test_correct/len(test_data)))

    x = range(1, epochs+1)

    # plt.figure(1)
    # plt.plot(x, inner, label="Inner Layer")
    # plt.plot(x, outer, label="Outer Layer")
    # plt.legend()
    # plt.xlabel('Epoch')
    # plt.ylabel('Weight Mean Value')

    plt.figure(2)
    for l in range(1, N_HIDDEN+1):
        plt.plot(x, gradient[l], label=f'Layer {l}')
    plt.xlabel('Epoch')
    plt.ylabel('Gradient Avg Value')
    plt.legend()

    # plt.figure(3)
    # train_x, train_y = zip(*train_A)
    # test_x, test_y = zip(*test_A)
    # plt.plot(train_x, train_y, label='Train Acc')
    # plt.plot(test_x, test_y, label='Test Acc')
    # plt.xlabel('Epoch')
    # plt.ylabel('Accuracy')
    # plt.legend()

    plt.show()

def fill_DNN(network, better=False, l=1):
    weights, biases = [None], [None]
    if better:
        for i in range(1, len(network)):
            rows = network[i]
            temp_w, temp_b = (rows*network[i-1] + network[i-1])/2, (rows + 1)/2
            r_w, r_b = (3/temp_w)**0.5, (3/temp_b)**0.5
            weights.append(2*r_w*np.random.rand(rows, network[i-1])-r_w)
            biases.append(2*r_b*np.random.rand(rows, 1)-r_b)
    else:
        for i in range(1, len(network)):
            weights.append(2*l*np.random.rand(network[i], network[i-1]) - l)
            biases.append(2*l*np.random.rand(network[i], 1)- l)
            
    return weights, biases

w, b = fill_DNN(network, better=True)
DNN(w, b)
