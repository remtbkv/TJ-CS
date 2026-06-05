import pandas as pd
from sklearn.naive_bayes import CategoricalNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, roc_auc_score, average_precision_score, matthews_corrcoef, PrecisionRecallDisplay
import numpy as np
import matplotlib.pyplot as plt


RAND_STATE = 2
ordinal_encoder = preprocessing.OrdinalEncoder()
label_encoder = preprocessing.LabelEncoder()


def read_ds(name):
    train_df = pd.read_csv(f"{name}_train.csv", header=0)
    names = train_df.columns
    features, output = names[:-1], names[-1]
    X_train = ordinal_encoder.fit_transform(train_df.loc[:, features])
    y_train = label_encoder.fit_transform(train_df.loc[:, [output]])

    test_df = pd.read_csv(f"{name}_test.csv", header=0)
    X_test = ordinal_encoder.fit_transform(test_df.loc[:, features])
    y_test = label_encoder.fit_transform(test_df.loc[:, [output]])
    return X_train, y_train, X_test, y_test, features

def test_solution(name, solution):
    X_train, y_train, X_test, y_test, _ = read_ds(name)
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pos = model.predict(X_test)
    print(f"Accuracy: {model.score(X_test, y_test)}")
    print(f"MCC: {matthews_corrcoef(y_test, y_pos)}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_pos)}")
    print(f"PR-AUC: {average_precision_score(y_test, y_pos)}")
    matrix = confusion_matrix(y_test, y_pos)
    print("Confusion matrix: ")
    print(matrix)

def PRC(name, solution):
    fig, ax = plt.subplots()
    X_train, y_train, X_test, y_test, _ = read_ds(name)
    models= [RandomForestClassifier(n_estimators=solution[0],
                                       max_depth=solution[1],
                                       max_features=solution[2],
                                       max_samples=solution[3],
                                       criterion=["gini", "entropy", "log_loss"][solution[4]],
                                       random_state=RAND_STATE),
            DecisionTreeClassifier(),
            CategoricalNB(),
            RandomForestClassifier()]
    names = ["PPMMAS-RF", "Decision-Tree", "NaiveBayes", "RF"]
    for i, model in enumerate(models):
        model.fit(X_train, y_train)
        y_pos = model.predict(X_test)
        #PrecisionRecallDisplay.from_predictions(y_train, y_pred_train, ax=ax)
        PrecisionRecallDisplay.from_predictions(y_test, y_pos, ax=ax, name=names[i])
    plt.title("Figure 2")
    plt.show()

def barchart(name, solution):
    X_train, y_train, X_test, y_test, _ = read_ds(name)
    models= [RandomForestClassifier(n_estimators=solution[0],
                                       max_depth=solution[1],
                                       max_features=solution[2],
                                       max_samples=solution[3],
                                       criterion=["gini", "entropy", "log_loss"][solution[4]],
                                       random_state=RAND_STATE),
            DecisionTreeClassifier(),
            CategoricalNB(),
            RandomForestClassifier()]
    names = ["PPMMAS-RF", "Decision-Tree", "NaiveBayes", "RF"]
    metrics = {"Accuracy": [], "MCC": [], "PR-AUC": []}
    for model in models:
        model.fit(X_train, y_train)
        y_pos = model.predict(X_test)
        metrics["Accuracy"].append(model.score(X_test, y_test))
        metrics["MCC"].append(matthews_corrcoef(y_test, y_pos))
        metrics["PR-AUC"].append(average_precision_score(y_test, y_pos))
        
    x = np.arange(len(names))
    width = 0.25
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')

    for attr, measurement in metrics.items():
        offset = width*multiplier
        rects = ax.bar(x+offset, measurement, width, label=attr)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    
    ax.set_ylim(0, 1)
    ax.set_title('Figure 3')
    ax.set_xticks(x+width, names)
    ax.legend(loc="upper right", ncols = 4)

    plt.show()

#test_solution("autism", [])
#PRC("autism", [60, 6, 1, 330, 0])
barchart("autism", [60, 6, 1, 330, 0])