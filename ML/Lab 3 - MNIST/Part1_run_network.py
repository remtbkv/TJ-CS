import numpy as np
from matplotlib import pyplot as plt

def p_net(A_vec, w, b, x):
    a, N = {0: x}, len(w)-1
    for layer in range(1, N+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[N]

def A(x):
    return 1/(1+np.exp(-x))

def Adx(x):
    return A(x)*(1-A(x))

a_vec = np.vectorize(A)
adx_vec = np.vectorize(Adx)
learn = 0.5
epochs = 1000
graph = []

def back_prop(weights, biases, start=0, learn=learn, A_vec=a_vec, Adx_vec=adx_vec, epochs=epochs):
    w, b = [None]+[i.copy() for i in weights[1:]], [None]+[i.copy() for i in biases[1:]]
    for e in range(start, epochs):
        a, dot, delta, N = {}, {}, {}, len(w)-1
        x, y = np.array([[0.05], [0.1]]), np.array([[0.01], [0.99]])
        
        out = p_net(a_vec, w, b, x)
        error = 1/2*((out-y)**2).sum()
        # graph.append((e,error))

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
            b[l] += learn*delta[l]
            w[l] += (learn*delta[l]) * a[l-1].T
        graph.append((w[1][0][0], error))
    return error

l1_weights, l2_weights = np.array([[0.15, 0.2], [0.25, 0.3]]), np.array([[0.4, 0.45], [0.5, 0.55]])
l1_biases, l2_biases = np.array([[0.35], [0.35]]), np.array([[0.6], [0.6]])
weights = [None, l1_weights, l2_weights]
biases = [None, l1_biases, l2_biases]

e = back_prop(weights, biases)
print("Final error:", e)

def plot(x_axis):
    x_vals, y_vals = zip(*graph)
    plt.plot(x_vals, y_vals)
    plt.xlabel(x_axis)
    plt.ylabel('Error')
    plt.title(f'How Error changes with {x_axis}')
    plt.show()

# plot("Epochs")
plot("w[1][0][0]")