import pickle, random, os
import numpy as np
from scipy.ndimage import rotate

store_file = "store_info2"
# learn = 0.0001
# learn = 0.05
# learn = 1
learn = 10
save_file = f"saved_info_{learn}"
epochs = 10

def save_info(*info):
    if os.path.exists(save_file):
        with open(save_file, 'rb') as f:
            lst = pickle.load(f)
    else:
        lst = []
    lst.append(info)
    with open(save_file, 'wb') as f:
        pickle.dump(lst, f)

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

# vectorized functions to work with np arrays
a_vec = np.vectorize(A)
adx_vec = np.vectorize(Adx)

def back_prop(data, initial_weights, initial_biases, start_epoch=0, learn=learn, A_vec=a_vec, Adx_vec=adx_vec, total_epochs=epochs):
    w, b = [None]+[i.copy() for i in initial_weights[1:]], [None]+[i.copy() for i in initial_biases[1:]]
    for epoch in range(start_epoch, total_epochs):
        # train = jitter(data) # distortion
        train = data # normal
        a, dot, delta, N = {}, {}, {}, len(network)-1
        for x, y in train:
            a[0] = x # define input layer
            for l in range(1, N+1):
                dot[l] = w[l]@a[l-1] + b[l] # calculate: wp+b
                a[l] = A_vec(dot[l]) # evaluate: f(wp+b)
            
            # delta[N] = (np.eye(y.shape[0]) + (-1 * a[N])) @ y # Gen AI
            delta[N] = Adx_vec(dot[N])*(y-a[N]) # normal

            # backprop
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            for l in range(N-1, 0, -1):
                delta[l] = Adx_vec(dot[l])*(w[l+1].T @ delta[l+1])
            
            # update weights/biases
            for l in range(1, N+1):
                b[l] += learn*delta[l]
                w[l] += (learn*delta[l]) * a[l-1].T
        
        misclassified = sum(1 for x, y in test_data if np.argmax(p_net(A_vec, w, b, x)) != np.argmax(y))
        accuracy = round((1-misclassified/len(test_data))*100,3)
        error = round((misclassified/len(test_data))*100,3)
        weight_val = w[1][0][0]
        gradient_error = delta[1][0][0]
        # dump_info(w, b, epoch) # store progress
        save_info(epoch, misclassified, accuracy, error, weight_val, gradient_error, w, b) # to graph later
        
        print("Epoch:", epoch)
        print("Misclassified:", misclassified)
        print(f"Accuracy: {accuracy}%")
        print(f"Error: {error}%")
        print("w[1][0][0]:",weight_val)
        print()
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

data = load_train()
# try:
#     w, b, e = load_info()
# except:
#     w, b = fill_network(network)
#     e = 0 

# fresh start
w, b = fill_network(network)
e = 0
print("Learning rate:", learn)
print()
back_prop(data, w, b, start_epoch=e)