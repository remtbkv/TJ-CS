from numpy.random import choice

def ppmmas(nants, rho, beta, graph, start_nodes, heuristic_function, evaluation_function, display_function, niterations = 10000, xi = 0., min_prey = 0, circular=True, return_history = False): #all parameter values chosen according to standard theory
    tau_max = 0 
    tau_min = 0 #both tau min and tau max will be updated dynamically, initial values dont matter
    N = .5 #controls strength of tau_min, small value to encourage exploitation
    stopping_threshold = 1e-100
    stopping_history = 1000
    past = [] #stopping conditions
    history = []

    pheromone_graph = {node:[1e5 for _ in graph[node]] for node in graph} #initialize pheromones to arbitrarily large value, will be fixed to tau_max after first iteration
    
    global_best = []
    global_eval = -1
    for itr in range(niterations):
        heuristic_graph = {node:[pheromone_graph[node][idx] * heuristic_function(node, graph[node][idx])**beta for idx in range(len(graph[node]))] for node in graph} #formulation for tau(t) * eta ** beta

        best_solution = []
        best_prey_solution = []
        best_eval = -1 #keep track of best solution so far in iteration
        best_prey_eval = -1
        predator_threshold = min(int(nants*(1-xi**(1+itr/5))), nants-min_prey)
        predator_traversed = dict()

        for ant in range(nants):
            if ant < predator_threshold: #predators follow mmas, exploit known solutions
                curridx = choice(range(len(start_nodes)))
                curr_node = start_nodes[curridx]
                solution = [(curridx, curr_node)]
                visited = {curr_node} #should be same as solution, unordered for constant access time
                while graph[curr_node]: #while there are nodes to be traversed
                    values = []
                    for idx, node in enumerate(graph[curr_node]):
                        if node not in visited: values.append(idx)
                    if not values: #all nodes have been visited already
                        break 
                    probs = [heuristic_graph[curr_node][idx] for idx in values]
                    tot = sum(probs)
                    nidx = choice(values, p=[x/tot for x in probs])
                    if xi:
                        pair = (curr_node, graph[curr_node][nidx])
                        if pair not in predator_traversed:
                            predator_traversed[pair] = 0
                        predator_traversed[pair] += 1
                    curr_node = graph[curr_node][nidx] #choose next node probabilistically based on heuristic measure
                    visited.add(curr_node)
                    solution.append((nidx, curr_node)) #add new node to visited
                if circular: solution[0] = (graph[solution[-1][1]].index(solution[0][1]), solution[0][1])
                curr_eval = evaluation_function(solution) #evaluate the current solution
                if curr_eval > best_eval:
                    best_eval = curr_eval
                    best_solution = solution #update iteration best
                    if curr_eval > global_eval:
                        if curr_eval > global_eval:
                            #print(display_function(global_eval), global_best)
                            pass
                        global_eval = curr_eval #update global best
                        global_best = best_solution
            else: #prey ant, explore unknown solutions
                curridx = choice(range(len(start_nodes)))
                curr_node = start_nodes[curridx]
                solution = [(curridx, curr_node)]
                visited = {curr_node} 
                while graph[curr_node]:
                    values = []
                    for idx, node in enumerate(graph[curr_node]):
                        if node not in visited: values.append(idx)
                    if not values: 
                        break
                    probs = [heuristic_graph[curr_node][idx] for idx in values]
                    for idx, nodeidx in enumerate(values):
                        if (pair:=(curr_node, graph[curr_node][nodeidx])) in predator_traversed:
                            probs[idx] *= 1/(1+predator_traversed[pair]**(predator_threshold/nants)) #update phereomones based on predator location
                    tot = sum(probs)
                    nidx = choice(values, p=[x/tot for x in probs])
                    pair = (curr_node, graph[curr_node][nidx])
                    if pair not in predator_traversed:
                        predator_traversed[pair] = 0
                    predator_traversed[pair] += 1
                    curr_node = graph[curr_node][nidx] 
                    visited.add(curr_node)
                    solution.append((nidx, curr_node)) 
                if circular: solution[0] = (graph[solution[-1][1]].index(solution[0][1]), solution[0][1])
                curr_eval = evaluation_function(solution)
                if curr_eval > best_eval:
                    best_eval = curr_eval
                    best_solution = solution
                    if curr_eval > global_eval:
                        #print(display_function(global_eval), global_best)
                        global_eval = curr_eval
                        global_best = best_solution
                if curr_eval > best_prey_eval:
                    best_prey_eval = curr_eval
                    best_prey_solution = solution

        past.append(global_eval)
        history.append(global_eval)
        if len(past) > stopping_history:
            past.pop(0)
            if past[-1]-past[0] < stopping_threshold:
                break
        
        tau_max = global_eval/rho
        n = len(graph)
        tau_min = tau_max*(1-(0.05)**(1/n))/((n/2-1)*(0.05)**(1/n))
        for idx, component in enumerate(best_solution):
            if idx != len(solution)-1:
                pheromone_graph[component[-1]][best_solution[idx+1][0]] += global_eval/rho 
            else:
                if circular: pheromone_graph[component[-1]][best_solution[0][0]] += global_eval/rho
        if xi:
            for idx, component in enumerate(best_prey_solution): #best prey addendum
                if idx != len(solution)-1:
                    pheromone_graph[component[-1]][best_prey_solution[idx+1][0]] += global_eval/rho * xi/10
                else:
                    if circular: pheromone_graph[component[-1]][best_prey_solution[0][0]] += global_eval/rho * xi/10
            for idx, component in enumerate(global_best): #best global addendum
                if idx != len(solution)-1:
                    pheromone_graph[component[-1]][global_best[idx+1][0]] += global_eval/rho * 1e-1
                else:
                    if circular: pheromone_graph[component[-1]][global_best[0][0]] += global_eval/rho * 1e-1
        for node in pheromone_graph:
            for idx in range(len(pheromone_graph[node])):
                pheromone_graph[node][idx] = max(min((1-rho)*pheromone_graph[node][idx], tau_max), tau_min) 
        print(f"Iteration {itr}: shortest_tour: {display_function(global_eval)}, iteration_best: {display_function(best_eval)}, prey_best: {display_function(best_prey_eval)}, tauMax: {tau_max}, tauMin: {tau_min}")
    if return_history:
        return global_best, global_eval, history
    return global_best, global_eval