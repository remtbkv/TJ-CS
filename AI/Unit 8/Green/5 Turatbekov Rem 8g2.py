import sys

# bits, funct_num = int(sys.argv[1]), int(sys.argv[2])

l = 1
num_epochs = 1000

def truth_table(bits, num):
    table = [tuple(map(int, i)) for i in reversed([format(i, '0' + str(bits) + 'b') for i in range(1 << bits)])]
    return list(zip(table, [int(i) for i in f"{num:08b}"[-len(table):]]))

def print_tt(bits, table):
    start = "  ".join([f"In{n}" for n in range(1, bits+1)])+"  |  Out"
    print(start+"\n"+"-"*len(start))
    for inp, out in table:
        print("", "    ".join(map(str, inp)), "  | ", str(out))

def step(num):
    return 1 if num>0 else 0

def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def scale(n, x):
    return tuple(n*i for i in x)

def add(a, b):
    return tuple(a[i]+b[i] for i in range(len(a)))

def perceptron(A, w, b, x):
    return A(dot(w, x) + b)

def update_weight(w, f, f_est, x):
    return add(w, scale((f-f_est)*l,x))

def update_bias(b, f, f_est):
    return b + (f-f_est)*l

def train(bits, funct_num):
    b, w, ttable = 0, tuple(0 for _ in range(bits)), truth_table(bits, funct_num)
    for _ in range(1, num_epochs):
        weights, biases = set(), set()
        weights.add(w)
        biases.add(b)
        for x, f in ttable:
            f_est = perceptron(step, w, b, x)
            w2, b2 = update_weight(w, f, f_est, x), update_bias(b, f, f_est)
            weights.add(w2)
            biases.add(b2)
            w, b = w2, b2
        if len(weights)==1 and len(biases)==1:
            break

    accuracy = sum(1 for x, f in ttable if f==perceptron(step, w, b, x))/len(ttable)
    # print("Final weight:",w)
    # print("Final bias:",b)
    # print("Accuracy:",accuracy)
    return accuracy

def task(bits):
    n = 2**bits
    good = sum(1 for i in range(2**n) if train(bits, i) == 1)
    print("Total:",2**n)
    print("100%:", good)

task(4)
# train(bits, funct_num)