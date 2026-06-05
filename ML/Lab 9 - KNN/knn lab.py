from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt



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


def knn(x, k, X,Y):
    ed = lambda a,b: np.sum(np.square(a - b))
    dist = [ed(x, x_train) for x_train in X]
    labels = [Y[i] for i in np.argsort(dist)[:k]]
    return np.argmax(np.bincount(labels))


# RANDOM_STATE = 42

# x1,y1 = zip(*first)
# plt.scatter(x1,y1, color='orange', label="0")
# x2,y2 = zip(*second)
# plt.scatter(x2,y2, color='blue', label="1")
# plt.legend()
# plt.show()


for rs in range(1,101):
    RANDOM_STATE = rs

    first, _ = datasets.make_blobs(n_samples=50, n_features=2, centers=1, center_box=(-13,-12), cluster_std=4, random_state=RANDOM_STATE)
    second, _ = datasets.make_blobs(n_samples=5000, n_features=2, centers=1, center_box=(-7,-6), cluster_std=2, random_state=RANDOM_STATE)
    fY, sY = [0 for _ in range(len(first))], [1 for _ in range(len(second))]
    newX, newY = np.concatenate((first, second)), np.concatenate((fY, sY))
    X_train, X_test, y_train, y_test = train_test_split(newX, newY, test_size=0.2, random_state=RANDOM_STATE)
    
    a = 0
    for i in X_test:
        a += knn(i, 22, X_train, y_train)
    a /= len(X_test)

    print("Random state =", rs)
    print("Accuracy:",a)
    print()
