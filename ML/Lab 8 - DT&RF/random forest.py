import math, random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from decision_tree import classify, get_most_common_labels, entropy, gain_ratio


"""
Psuedocode:

select N random samples of K rows from the data, with repalcement
 - N should ideally be a very high number (~1000)
 - K usually is length of data
for each sample, build a decision tree
  - select random subset of features (sqrt num of features) to split on, at each split
to make predictions, pass test sample through each tree and majority vote the results
"""

def make_tree(data, attributes, VALS, most_common_labels):
    if not entropy(data) or not attributes:
        return data.iloc[:, -1].mode()[0]
    random_features = random.sample(attributes, math.isqrt(len(attributes)))
    tree, children, best_var = {}, {}, max(random_features, key=lambda c: gain_ratio(data, c))
    attributes.remove(best_var)
    for val in VALS[best_var]:
        if val in data[best_var].unique():
            next_data = data[data[best_var] == val].drop(columns=best_var)
            children[val] = make_tree(next_data, attributes, VALS, most_common_labels)
        else:
            children[val] = most_common_labels[best_var][val]
    tree[best_var] = children
    return tree

def make_tree_print(data, attributes, VALS, most_common_labels, n=0):
    if not entropy(data) or not attributes:
        return data.iloc[:, -1].mode()[0]
    random_features = random.sample(attributes, math.isqrt(len(attributes)))
    tree, children, space, best_var = {}, {}, " "*n+"*  ", max(random_features, key=lambda c: gain_ratio(data, c))
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

def make_forest(data, VARS, VALS, mcl, num_trees):
    random_samples = [data.sample(n=len(data), replace=True, random_state=RANDOM_STATE) for _ in range(num_trees)]
    return [make_tree(s, VARS.copy(), VALS, mcl) for s in random_samples]

def mine(fn, num_trees=100, test_accuracy=False):
    data = pd.read_csv(fn)
    VARS = list(data.columns[:-1])
    VALS = {var: data[var].unique() for var in VARS}
    mcl = get_most_common_labels(data, VARS, VALS)
    X_train, X_test, y_train, y_test = train_test_split(data, data.iloc[:, -1], test_size=0.2, random_state=RANDOM_STATE)
    forest = make_forest(X_train, VARS, VALS, mcl, num_trees)
    predictions = [pd.Series([classify(tree, sample, VARS) for tree in forest]).mode()[0] for sample in X_test.values]
    accuracy = accuracy_score(y_test, predictions)
    cm = pd.DataFrame(confusion_matrix(y_test, predictions), index=['Actual Negative', 'Actual Positive'], columns=['Predicted Negative', 'Predicted Positive'])
    if test_accuracy:
        return accuracy
    else:
        print("Accuracy:", accuracy)
        print("Confusion Matrix:\n", cm)

def existing(fn, num_trees=100, test_accuracy=False):
    data = pd.read_csv(fn)
    label_encoders = {}
    for column in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    rf = RandomForestClassifier(random_state=RANDOM_STATE, n_estimators=num_trees)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
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
        print(i)
        global RANDOM_STATE
        RANDOM_STATE = i
        ma += mine(fn, test_accuracy=True)
        ea += existing(fn, test_accuracy=True)
    print("Mine:", ma/100)
    print("Existing:", ea/100)


if __name__ == "__main__":
    global RANDOM_STATE
    RANDOM_STATE = 42
    random.seed(RANDOM_STATE)

    fn = 'diabetes_discretized.csv'

    # test_acc(fn)

    print("My Decision Tree:")
    mine(fn)
    print("\nExisting Decision Tree:")
    existing(fn)
