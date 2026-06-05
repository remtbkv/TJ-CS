from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

RANDOM_STATE = 42

def mine(k):
    irisDS = datasets.load_iris()
    ft, lb = irisDS.data, irisDS.target
    X_train, X_test, y_train, y_test = train_test_split(ft, lb, test_size=0.2, random_state=RANDOM_STATE)
    def knn(x, k):
        ed = lambda a, b: np.sum(np.square(a - b)) 
        dist = [ed(x, xt) for xt in X_train]
        labels = [y_train[i] for i in np.argsort(dist)[:k]]
        return np.argmax(np.bincount(labels))
    
    return sum([knn(x,k)==y_test[i] for i, x in enumerate(X_test)])/len(X_test)

def existing(k):
    irisDS = datasets.load_iris()
    ft, lb = irisDS.data, irisDS.target
    X_train, X_test, y_train, y_test = train_test_split(ft, lb, test_size=0.2, random_state=RANDOM_STATE)
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    return accuracy_score(y_test, y_pred)

accuracy = [(k, mine(k), existing(k)) for k in range(1,101)]
print(accuracy)