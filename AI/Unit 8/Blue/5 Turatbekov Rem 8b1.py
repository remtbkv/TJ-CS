import matplotlib.pyplot as plt

bits = 2

l, num_epochs = 1, 100


def truth_table(bits, num):
    table = [tuple(map(int, i)) for i in reversed([format(i, '0' + str(bits) + 'b') for i in range(1 << bits)])]
    return list(zip(table, [int(i) for i in f"{num:08b}"[-len(table):]]))


def step(num):
    return 1 if num > 0 else 0


def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))


def scale(n, x):
    return tuple(n*i for i in x)


def add(a, b):
    return tuple(a[i]+b[i] for i in range(len(a)))


def perceptron(A, w, b, x):
    return A(dot(w, x) + b)


def update_weight(w, f, f_est, x):
    return add(w, scale((f-f_est)*l, x))


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
        if len(weights) == 1 and len(biases) == 1:
            break

    return w, b


def axis_range(start, stop, step):
    l = []
    while start < stop:
        l.append(round(start, 1))
        start += step
    return l


def plot_graph(funct_num, w, b, ax):
    axis = axis_range(-2, 2.1, 0.1)
    # inequality coloring
    for x in axis:
        for y in axis:
            output = perceptron(step, w, b, (x, y))
            color = 'green' if output == 1 else 'red'
            ax.plot(x, y, 'o', color=color, markersize=2)
    # big points
    ttable = truth_table(bits, funct_num)
    for inp, out in ttable:
        color = 'green' if out == 1 else 'red'
        ax.plot(inp[0], inp[1], 'o', color=color, markersize=6)


def main():
    fig, axs = plt.subplots(4, 4, figsize=(10, 10))
    for funct_num in range(16):
        w, b = train(bits, funct_num)
        col, row = funct_num//4, funct_num%4
        ax = axs[col, row]
        plot_graph(funct_num, w, b, ax)
        
        ax.set_title(f'Function {funct_num}')
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)

    plt.tight_layout()
    plt.show()

main()
