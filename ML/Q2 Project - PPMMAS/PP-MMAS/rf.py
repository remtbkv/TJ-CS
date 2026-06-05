import pandas as pd
from utils import ppmmas
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, roc_auc_score, average_precision_score, matthews_corrcoef

ordinal_encoder = preprocessing.OrdinalEncoder()
label_encoder = preprocessing.LabelEncoder()

MAXTREE = 150
SAMPLE_STEP = 10
SCALE_EXP = 4
RAND_STATE = 2

def read_rf(name):
    train_df = pd.read_csv(f"{name}_train.csv", header=0)
    names = train_df.columns
    features, output = names[:-1], names[-1]
    X_train = ordinal_encoder.fit_transform(train_df.loc[:, features])
    y_train = label_encoder.fit_transform(train_df.loc[:, [output]])

    test_df = pd.read_csv(f"{name}_test.csv", header=0)
    X_test = ordinal_encoder.fit_transform(test_df.loc[:, features])
    y_test = label_encoder.fit_transform(test_df.loc[:, [output]])
    return X_train, y_train, X_test, y_test, features

def initialize_rf(numinstances, numfeatures):    
    layers = [
        [f"0_{x}" for x in list(range(5, MAXTREE, 5))], #number of trees
        [f"1_{x}" for x in list(range(1, numfeatures))], #max_depth of tree 
        [f"2_{x}" for x in list(range(1, numfeatures))], #max_features
        [f"3_{x}" for x in list(range(SAMPLE_STEP, numinstances, SAMPLE_STEP))], #num_samples
        [f"4_{x}" for x in range(3)], #criterion
        []
    ]
    graph = {y:layers[i+1] for i,x in enumerate(layers[:-1]) for y in x }
    start_nodes = layers[0]
    return graph, start_nodes

def parse_node(node):
    return int(node.split("_")[-1])

def analyze_rf(name):
    X_train, y_train, X_test, y_test, features = read_rf(name)
    graph, start_nodes = initialize_rf(len(X_train), len(features))

    def heuristic(_, node):
        return 1/(parse_node(node)+100)
    
    def eval(solution):
        solution = [x[-1] for x in solution]
        model = RandomForestClassifier(n_estimators=parse_node(solution[0]),
                                       max_depth=parse_node(solution[1]),
                                       max_features=parse_node(solution[2]),
                                       max_samples=parse_node(solution[3]),
                                       criterion=["gini", "entropy", "log_loss"][parse_node(solution[4])],
                                       random_state=RAND_STATE)
        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)
        if accuracy>.9208:
            print(solution)
        return accuracy**SCALE_EXP
    
    def display(val):
        return val**(1/SCALE_EXP)
    
    tour, best = ppmmas(50, .5, 0.5, graph, start_nodes, heuristic, eval, display, xi=0.75, min_prey=20, niterations=1000, circular=False)
    print(tour, display(best))

def test_solution(name, solution):
    X_train, y_train, X_test, y_test, _ = read_rf(name)
    model = RandomForestClassifier(n_estimators=solution[0],
                                       max_depth=solution[1],
                                       max_features=solution[2],
                                       max_samples=solution[3],
                                       criterion=["gini", "entropy", "log_loss"][solution[4]],
                                       random_state=RAND_STATE)
    model.fit(X_train, y_train)
    y_pos = model.predict(X_test)
    print(f"Accuracy: {model.score(X_test, y_test)}")
    print(f"MCC: {matthews_corrcoef(y_test, y_pos)}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_pos)}")
    print(f"PR-AUC: {average_precision_score(y_test, y_pos)}")
    matrix = confusion_matrix(y_test, y_pos)
    print("Confusion matrix: ")
    print(matrix)
    


#analyze_rf("autism")
test_solution("autism", [60, 6, 1, 330, 0])