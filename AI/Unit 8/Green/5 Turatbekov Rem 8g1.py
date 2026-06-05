import sys, ast
funct_num, scalar_b = int(sys.argv[1]), float(sys.argv[3])
vector_w = ast.literal_eval(sys.argv[2])
bits = len(vector_w)

def truth_table(bits, num):
    table = [tuple(map(int, i)) for i in reversed([format(i, '0' + str(bits) + 'b') for i in range(1<<bits)])]
    return list(zip(table, [int(i) for i in f"{num:08b}"[-len(table):]]))

def pretty_print_tt(table):
    start = "  ".join([f"In{n}" for n in range(1, bits+1)])+"  |  Out"
    print(start+"\n"+"-"*len(start))
    for inp, out in table:
        print("","    ".join(map(str, inp)),"  | ",str(out))


def dot(a, b):
    return sum(a[i]*b[i] for i in range(len(a)))

def perceptron(A, w, b, x):
    return A(dot(w,x) + b)

def step(num):
    return 1 if num>0 else 0

def check(n, w, b):
    ttable = truth_table(n, funct_num)
    correct = sum(1 for inp,out in ttable if perceptron(step, w, b, inp)==out)
    return correct/len(ttable) 

print(check(bits, vector_w, scalar_b))