from utils import ppmmas
import matplotlib.pyplot as plt

def read_weights(filename):
    with open(filename, "r") as f:
        weightmatrix = [list(map(int, filter(lambda x: x!="" and x!="\n", x.split(" ")))) for x in f.readlines()]
    return weightmatrix

def read_tsp(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    coords = {}
    start_nodes = []
    for line in lines:
        node, x, y = map(int, line.split(" "))
        coords[node] = (x, y)
        start_nodes.append(node)
    graph = {node: [x for x in start_nodes if x != node] for node in start_nodes}
    return coords, start_nodes, graph

def get_dist(snode, node, matrix = None, coords = None):
    if matrix:
        return matrix[snode][node]
    return ((coords[snode][0] - coords[node][0])**2 + (coords[snode][1] - coords[node][1])**2)**0.5

def initialize_tsp(filename):
    weights = read_weights(filename)
    start_nodes = list(range(len(weights)))
    graph = {node: [x for x in start_nodes if x != node] for node in start_nodes}
    return weights, start_nodes, graph
    
def analyze_tsp(file, solfile=None, tspformat = False, xi=0, nitr = 1000):
    weights = None
    coords = None
    if not tspformat:
        weights, start_nodes, graph = initialize_tsp(file)
    else:
        coords, start_nodes, graph = read_tsp(file)

    def heuristic(snode, enode):
        return 1/get_dist(snode, enode, weights, coords)
    
    def eval(solution):
        return 1/ (sum([get_dist(solution[i][1], solution[i+1][1], weights, coords) for i in range(len(solution)-1)]) + get_dist(solution[-1][1], solution[0][1], weights, coords))
    
    def display(val):
        return 1/val
    
    if solfile:
        with open(solfile, "r") as f:
            true_sol = [x-1 for x in map(int, filter(lambda x: x!="\n", f.readlines()))]
        true_length = (sum([get_dist(true_sol[i], true_sol[i+1], weights, coords) for i in range(len(true_sol)-1)]) + get_dist(true_sol[-1], true_sol[0], weights, coords))
    else:
        true_length = 21281.57
    #print(true_length)
    tour, best, history = ppmmas(100, .5, 5, graph, start_nodes, heuristic, eval, display, xi=xi, min_prey=0, niterations=nitr, return_history=True)
    print(tour, 1/best, (1/best-true_length)/true_length)
    return history

def xiplot(file, solfile=None, tspformat = False):
    true_length = 21281.57
    
    for xi in [0, 0.2, 0.4, 0.6, 0.8]:
        hist = [(1/x-true_length)/true_length for x in analyze_tsp(file, solfile, tspformat, xi, 100)]
        plt.plot(list(range(100)), hist, label=f"xi: {xi}")

    plt.title("Figure 1")
    plt.legend()
    plt.xlabel("No. tour constructions")
    plt.ylabel("percentage deviation")
    plt.show()


#analyze_tsp("kroA100.txt",tspformat=True)
xiplot("kroA100.txt",tspformat=True)