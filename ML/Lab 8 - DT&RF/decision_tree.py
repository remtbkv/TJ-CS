import math
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

def entropy(data):
    probs = data.iloc[:, -1].value_counts(normalize=True)
    return -sum(probs * probs.map(math.log2))

def smaller_data(data, var):
    return [data[data[var] == value] for value in data[var].unique()]

def gain(data, var):
    return entropy(data) - sum([entropy(subset)*len(subset)/len(data) for subset in smaller_data(data, var)])

def gain_ratio(data, var):
    spl = -sum([(n := len(subset)/len(data))*math.log(n, 2) for subset in smaller_data(data, var)])
    return  gain(data, var)/spl if spl else 0

def printer(tree):
    for k, v in tree.items():
        if type(v) == dict:
            print(k)
            printer(v)
        else:
            print(k+" --> "+v)

def classify(tree, vector, vars):
    node = tree.copy()
    while type(node) == dict:
        var = next(iter(node))
        val = vector[vars.index(var)]
        node = node[var][val]
    return node

def proper_string_split(s):
    n = s.count("-")-1
    return -n*float(s[1:].split("-")[n])

def make_tree_print(data, attributes, VALS, most_common_labels, n=0):
    if not entropy(data) or not attributes:
        return data.iloc[:, -1].mode()[0]
    tree, children, space, best_var = {}, {}, " "*n+"*  ", max(attributes, key=lambda c: gain_ratio(data, c))
    attributes.remove(best_var)
    for val in VALS[best_var]:
        child = " "*(n+2)+"*  "+str(val)
        if val in data[best_var].unique():
            next_data = data[data[best_var] == val].drop(columns=best_var)
            children[child] = make_tree_print(next_data, attributes, VALS, most_common_labels, n+4)
        else:
            children[child] = most_common_labels[best_var][val]
    tree[space+best_var + "? (entropy gain ratio: "+str(round(gain_ratio(data, best_var), 4))+")"] = children
    return tree

def make_tree(data, attributes, VALS, most_common_labels):
    if not entropy(data) or not attributes:
        return data.iloc[:, -1].mode()[0]
    tree, children, best_var = {}, {}, max(attributes, key=lambda c: gain_ratio(data, c))
    attributes.remove(best_var)
    for val in VALS[best_var]:
        if val in data[best_var].unique():
            next_data = data[data[best_var] == val].drop(columns=best_var)
            children[val] = make_tree(next_data, attributes, VALS, most_common_labels)
        else:
            children[val] = most_common_labels[best_var][val]
    tree[best_var] = children
    return tree

def sorted_tree(tree):
    if type(tree) != dict:
        return tree
    var, children = list(tree.items())[0]
    sorted_keys = sorted(children.keys(), key=lambda c: proper_string_split(cleaned(c)))
    return {var: {k: sorted_tree(children[k]) for k in sorted_keys}}

def cleaned(s):
    s1 = s.split("?")[0]
    return s1.split("*")[1].strip() if "*" in s1 else s1

def get_most_common_labels(data, VARS, VALS):
    return {var: {val: data[data[var] == val].iloc[:, -1].mode()[0] for val in VALS[var]} for var in VARS}

def mine(fn, show=False, test_accuracy=False, save_datasets=False):
    data = pd.read_csv(fn)
    VARS = list(data.columns[:-1])
    VALS = {var: data[var].unique() for var in VARS}
    X_train, X_test, y_train, y_test = train_test_split(data, data.iloc[:,-1], test_size=0.2, random_state=RANDOM_STATE)
    if save_datasets:
        X_train.to_csv('X_train.csv', index=False)
        X_test.to_csv('X_test.csv', index=False)
    mcl = get_most_common_labels(X_train, VARS, VALS)
    tree = make_tree(X_train, VARS.copy(), VALS, mcl)
    if show:
        t = make_tree_print(X_train, VARS.copy(), VALS, mcl)
        if fn == 'diabetes_discretized.csv':
            printer(sorted_tree(t))
        else:
            printer(t)
        print()
    predictions = [classify(tree, vector, VARS) for vector in X_test.values]
    accuracy = accuracy_score(y_test, predictions)
    cm = pd.DataFrame(confusion_matrix(y_test, predictions), index=['Actual Negative', 'Actual Positive'], columns=['Predicted Negative', 'Predicted Positive'])
    if test_accuracy:
        return accuracy
    else:
        print("Accuracy:", accuracy)
        print("Confusion Matrix:\n", cm)

def existing(fn, test_accuracy=False):
    data = pd.read_csv(fn)
    label_encoders = {}
    for column in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    clf = DecisionTreeClassifier(random_state=RANDOM_STATE)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = pd.DataFrame(confusion_matrix(y_test, y_pred), index=['Actual Negative', 'Actual Positive'], columns=['Predicted Negative', 'Predicted Positive'])
    if test_accuracy:
        return accuracy
    else:
        print("Accuracy:", accuracy)
        print("Confusion Matrix:\n", cm)

def test_acc(fn):
    ma, ea = 0, 0
    for i in range(100):
        global RANDOM_STATE
        RANDOM_STATE = i
        ma += mine(fn, test_accuracy=True)
        ea += existing(fn, test_accuracy=True)
    print("Mine:", ma/100)
    print("Existing:", ea/100)

if __name__ == "__main__":
    fn = 'diabetes_discretized.csv'
    RANDOM_STATE = 42
    # test_acc(fn)

    print("My Decision Tree:")
    mine(fn, show=True)
    print("\nExisting Decision Tree:")
    existing(fn)