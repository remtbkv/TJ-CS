import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron

LR = 0.01
NUM_EPOCHS = 100
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

"""
to be used in Q2 and Q3
features: sepal length, petal length 
classes: setosa (1), non-setosa (0)
"""
iris = load_iris()
X, y = iris.data[:, [0, 2]], (iris.target == 0).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)


def separation_line(x, y):
    return y>=0.8*x+0.2

def step(x):
    return 1 if x>0 else 0

def hard_threshold(x):
    return 1 if x >= 0 else 0

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def perceptron(A, w, b, X):
    return A(np.dot(w, X) + b)

def p_net(A_vec, w, b, x):
    a, n = {0: x}, len(w)-1
    for layer in range(1, n+1):
        a[layer] = A_vec(w[layer] @ a[layer-1] + b[layer])
    return a[n]

def update_weight(w, y, y_est, X):
    return tuple(w[i] + LR*(y-y_est)*X[i] for i in range(len(w)))

def update_bias(b, y, y_est):
    return b + (y-y_est)*LR

def train(data, num_epochs, act_f):
    # b, w = np.random.uniform(-1, 1), tuple(np.random.uniform(-1, 1) for _ in range(len(data[0][0])))
    b, w = 0, tuple(0 for _ in range(len(data[0][0])))
    for _ in range(num_epochs):
        weights, biases = set(), set()
        weights.add(w)
        biases.add(b)
        for X, y in data:
            y_est = perceptron(act_f, w, b, X)
            w2, b2 = update_weight(w, y, y_est, X), update_bias(b, y, y_est)
            weights.add(w2)
            biases.add(b2)
            w, b = w2, b2
        if len(weights)==1 and len(biases)==1:
            break
    return w,b

def decision_boundary(w, b, x):
    return -(w[0] * x + b) / w[1]

def test_rates(N=500):
    lrs = [10, 1, 0.1, 0.01, 0.001]
    for lr in lrs:
        global LR
        LR = lr
        q1(train_size=N, plot=False)

def q1(train_size=500, test_size=500, plot=True):
    # act_f = sigmoid
    act_f = hard_threshold
    X_train = np.random.rand(train_size, 2)
    y_train = np.where(separation_line(X_train[:, 0], X_train[:, 1]), 1, 0)
    train_data = list(zip(X_train, y_train))
    w, b = train(train_data, NUM_EPOCHS, act_f)
    
    X_test = np.random.rand(test_size, 2)
    y_test = np.where(separation_line(X_test[:, 0], X_test[:, 1]), 1, 0)
    test_data = list(zip(X_test, y_test))
    missed = []
    wrong = 0
    for inp, outp in test_data:
        if int(perceptron(act_f, w, b, inp)>=0.5) != outp:
            wrong += 1
            missed.append(inp)
    if missed:
        missed = np.vstack(missed)
        plt.scatter(missed[:, 0], missed[:, 1], color='orange', s=10, label=f"# Misclassified = {wrong}")
    print(f"Learning rate: {LR}\tMisclassified: {wrong}\ty={round(-w[0]/w[1], 3)}x+{round(-b/w[1], 3)}")
    if plot:
        plt.scatter(X_train[y_train == 1][:, 0], X_train[y_train == 1][:, 1], color='blue', label='Above (1)')
        plt.scatter(X_train[y_train == 0][:, 0], X_train[y_train == 0][:, 1], color='red', label='Below (0)')
        gx = np.linspace(0, 1, 100)
        plt.plot(gx, 0.8*gx+0.2, color='black', linestyle='dashed', label='True Line (y=0.8x+0.2)')
        plt.plot(gx, decision_boundary(w, b, gx), color='green', label=f'Perceptron Boundary (y={round(-w[0]/w[1],3)}x+{round(-b/w[1],3)})')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.legend()
        plt.show()

#############

def plot(X, y, w, b, compare=False, w2=None, b2=None):
    plt.scatter(X[y == 1][:, 0], X[y == 1][:, 1], color='blue', label='Setosa (1)')
    plt.scatter(X[y == 0][:, 0], X[y == 0][:, 1], color='red', label='Non-Setosa (0)')
    gx = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
    plt.plot(gx, decision_boundary(w, b, gx), color='green', label=f'Perceptron Boundary (y={round(-w[0]/w[1],3)}x+{round(-b/w[1],3)})')
    if compare:
        plt.plot(gx, decision_boundary(w2, b2, gx), color='pink', label=f'SciKit Perceptron Boundary (y={round(-w2[0]/w2[1],3)}x+{round(-b2/w2[1],3)})')
    plt.xlabel("Sepal Length")
    plt.ylabel("Petal Length")
    plt.title("Sepal Length vs Petal Length")
    plt.legend()
    plt.show()

def q2():
    act_f = sigmoid
    # act_f = hard_threshold
    train_data, test_data = list(zip(X_train, y_train)), list(zip(X_test, y_test))
    w, b = train(train_data, NUM_EPOCHS, act_f)
    test_correct = sum(y == (perceptron(act_f, w, b, X) >= 0.5) for X, y in test_data)
    test_acc = test_correct / len(test_data)
    print("Final weights:", w)
    print("Final bias:", b)
    print("Train Accuracy:", sum(y == (perceptron(act_f, w, b, X) >= 0.5) for X, y in train_data)/len(train_data))
    print("Test Accuracy:", test_acc)
    print("Test misclassified:", len(test_data)-test_correct)
    plot(X,y,w,b)

#############

def q3():
    perceptron = Perceptron(max_iter=NUM_EPOCHS, eta0=LR, random_state=RANDOM_STATE, tol=None, shuffle=False)
    perceptron.fit(X_train, y_train)
    train_acc, test_acc = perceptron.score(X_train, y_train), perceptron.score(X_test, y_test)
    test_misc = int((1-test_acc)*len(X_test))
    w, b = perceptron.coef_[0], perceptron.intercept_[0]
    print("Final weights:", w)
    print("Final bias:", b)
    print("Train Accuracy:", train_acc)
    print("Test Accuracy:", test_acc)
    print("Test misclassified:", test_misc)
    plot(X, y, w, b)

def compare_plots():
    act_f = sigmoid
    # act_f = hard_threshold
    train_data = list(zip(X_train, y_train))
    w, b = train(train_data, NUM_EPOCHS, act_f)

    perceptron = Perceptron(max_iter=NUM_EPOCHS, eta0=LR, random_state=RANDOM_STATE, tol=None, shuffle=False)
    perceptron.fit(X_train, y_train)
    w2, b2 = perceptron.coef_[0], perceptron.intercept_[0]

    plot(X, y, w, b, compare=True, w2=w2, b2=b2)

#############

def truth_table(bits):
    return [tuple(map(int, i)) for i in reversed([format(i, '0' + str(bits) + 'b') for i in range(1 << bits)])]

def print_tt(table):
    start = "  ".join([f"In{n}" for n in range(1, len(table[0][0])+1)])+"  |  Out"
    print(start+"\n"+"-"*len(start))
    for inp, out in table:
        print("", "    ".join(map(str, inp)), "  | ", str(out))

def q5a():
    global LR
    LR = 1
    OR = [((1, 1), 1), ((1, 0), 1), ((0, 1), 1), ((0, 0), 0)]
    AND = [((1, 1), 1), ((1, 0), 0), ((0, 1), 0), ((0, 0), 0)]
    NAND = [((1, 1), 0), ((1, 0), 1), ((0, 1), 1), ((0, 0), 1)]
    XOR = [((1, 1), 0), ((1, 0), 1), ((0, 1), 1), ((0, 0), 0)]
    XNOR = [((1, 1), 1), ((1, 0), 0), ((0, 1), 0), ((0, 0), 1)]
    to_train = {"OR": OR, "AND": AND, "NAND": NAND, "XOR": XOR, "XNOR": XNOR}
    act_f = hard_threshold
    for k, t_set in to_train.items():
        print(k)
        w, b = train(t_set, NUM_EPOCHS, act_f)
        out, correct = [], 0
        for X, y in t_set:
            if y == (output := perceptron(act_f, w, b, X)):
                correct += 1
            out.append((X, output))
        print_tt(out)
        print(f"Correct: {correct}/4\n")

def q5b(n=5):
    global LR
    LR = 1
    print(f"Using n = {n}:\n")
    act_f = hard_threshold
    tt_random = [(i, np.random.choice([0, 1])) for i in truth_table(n)]
    w, b = train(tt_random, NUM_EPOCHS, act_f)
    out, correct = [], 0
    for X, y in tt_random:
        if y == (output := perceptron(act_f, w, b, X)):
            correct += 1
        out.append((X, output))
    print_tt(out)
    print(f"Correct: {correct}/{2**n}")

#############

def run_network(x):
    transfer_vec = np.vectorize(hard_threshold)
    l1_weights = np.array([[-1, -1, 1, 1, -1],
                           [-1, 1, -1, 1, 1],
                           [-1, 1, 1, -1, -1],
                           [1, -1, -1, -1, 1],
                           [1, -1, 1, 1, 1],
                           [1, 1, -1, -1, 1]])
    l1_biases = np.array([[-2], [-3], [-2], [-2], [-4], [-3]])
    l2_weights = np.array([[1, 1, 1, 1, 1, 1]])
    l2_biases = np.array([[-1]])
    weights = [None, l1_weights, l2_weights]
    biases = [None, l1_biases, l2_biases]
    inp_vec = np.array(x).reshape(-1, 1)
    return p_net(transfer_vec, weights, biases, inp_vec)[0, 0]

def generalized(ttable):
    ones = [inp for inp, out in ttable if out]
    l1_weights = np.array([[1 if i else -1 for i in inp] for inp in ones])
    l1_biases = np.array([-sum(i) for i in ones]).reshape(-1,1)
    l2_biases = np.array([[-1]])
    l2_weights = np.array([[1]*len(ones)])
    weights = [None, l1_weights, l2_weights]
    biases = [None, l1_biases, l2_biases]
    return weights, biases

def run_general(A, w, b, x):
    inp_vec = np.array(x).reshape(-1, 1)
    return p_net(A, w, b, inp_vec)[0, 0]

def q6():
    # print(run_network([0,0,1,1,0]))
    # print(run_network([0,1,0,1,1]))
    # print(run_network([0,1,1,0,0]))
    # print(run_network([1,0,0,0,1]))
    # print(run_network([1,0,1,1,1]))
    # print(run_network([1,1,0,0,1]))
    tt_mine = [(inp, run_network(inp)) for inp in truth_table(5)] # my truth table
    # print_tt(tt_mine)
    weights, biases = generalized(tt_mine)

    print("Layer 2 Bias:")
    print(biases[2][0])
    print("\nLayer 2 Weights:")
    print(weights[2][0])
    print("\nLayer 1 Biases:")
    print(biases[1].flatten())
    print("\nLayer 1 Weights:")
    print(weights[1][0])
    print("\nInputs:")
    print(" ".join([f"x{i}" for i in range(1, len(weights[1][0])+1)]))
    print()
    A = np.vectorize(hard_threshold)
    tt_general = [(inp, run_general(A, weights, biases, inp)) for inp in truth_table(5)] # generalized truth table
    print(f"Do they make the same truth table?: {tt_mine==tt_general}")


print("Question 1:")
q1() # classify line
# test_rates(N=5000)
print("\nQuestion 2:")
q2() # iris manual implementation
print("\nQuestion 3:")
q3() # iris existing implementation
# compare_plots() # compare plots from q2 and q3
print("\nQuestion 5a:")
q5a() # binary functions
print("\nQuestion 5b:")
q5b(n=5) # test accuracies on general tables
print("\nQuestion 6:")
q6() # 1 layer MLP, generalized
