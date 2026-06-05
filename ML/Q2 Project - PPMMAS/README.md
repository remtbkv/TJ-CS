# PP-MMAS
Predator-Prey interactions within Max-Min Ant Systems (MMASs) for random forest hyperparameter optimization

Max-Min Ant Systems (MMASs), a variant on Ant Colony Optimizations (ACOs), show great promise in solving hard combinatorial and graph problems. Yet, the algorithm suffers from premature convergence on a suboptimal solution, primarily due to its prioritization of exploitation over exploration. In order to resolve this premature convergence, recent research has been done in improving the algorithm or exploring other variants of ACOs. In this paper, we present a novel investigation into introducing predator-prey interactions for MMASs, providing a dynamic balance between exploration and exploitation. A Predator-Prey Max-Min Ant System (PP-MMAS) differs from the normal MMAS in that a proportion of ants are labelled as “predators,” driving the remaining “prey” ants away from solutions already explored. The goal of this paper is to apply the algorithm to optimize hyperparameter selection for Random Forests, as well as test PP-MMAS on typical combinatorial benchmarks like the Traveling Salesman Problem (TSP). Hyperparamter optimization has been a long standing problem for parameter-dependent systems like Random Forest, and various swarm optimizations have been introduced to alleviate the issue. The parameters of a Random Forest can be generalized as nodes on a graph, applying the same concepts as TSP. Our computational results show that PP-MMAS performs just as well or better than MMAS in all TSP test cases. Classification is fairly competitive when compared to state-of-the-art classification models for ongoing autism research and diagnosis.

## Running the Code (PP-MMAS)
To run the PP-MMAS on code, open the tsp.py file and run the function **tsp_analyze()** on the file you wish to run it on:
```
analyze_tsp("kroA100.txt",tspformat=True)
```
The tspformat parameter controls whether or not the file is in tsp_format. kroA100 is, the rest are not.

To plot different values of xi, call the **xiplot()** function:
```
xiplot("kroA100.txt",tspformat=True)
```

## Running Random Forest Analysis
To run PP-MMAS on random forest, open the rf.py file and run the **analyze_tsp()** function:
```
analyze_rf("autism")
```

To test a specific set of parameters and analyze different metrics, call the **test_solution()** function:
```
test_solution("autism", [60, 6, 1, 330, 0])
```

## Credits
Submitted in completion of Q2 project, co-authored by Avery Li and Rem Turatbekov, TJHSST
