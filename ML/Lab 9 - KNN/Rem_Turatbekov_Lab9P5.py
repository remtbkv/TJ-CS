from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt


def knn(x, k, X, Y):
    ed = lambda a, b: np.sum(np.square(a - b))
    dist = [ed(x, x_train) for x_train in X]
    labels = [Y[i] for i in np.argsort(dist)[:k]]
    return np.argmax(np.bincount(labels))


RANDOM_STATE = 42
NUM_DATA = 200
NUM_OUTLIERS = int(NUM_DATA*0.2)
k = 22

def main():
    dataX, dataY = make_blobs(n_samples=NUM_DATA, n_features=2, centers=2, cluster_std=2, random_state=RANDOM_STATE)

    # DIRTY
    outlierX, outlierY = np.random.uniform(low=-15, high=15, size=(NUM_OUTLIERS, 2)), np.random.choice([0, 1], size=NUM_OUTLIERS)
    X, y = np.vstack([dataX, outlierX]), np.hstack([dataY, outlierY])
    zero, one = X[y == 0], X[y == 1]
    plt.scatter(zero[:, 0], zero[:, 1], color='blue', label='Label 0')
    plt.scatter(one[:, 0], one[:, 1], color='orange', label='Label 1')
    plt.title("Outlier Data")
    plt.legend()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    outlier_acc = np.mean([knn(x, k, X_train, y_train) == y_test[i] for i, x in enumerate(X_test)])
    print(f"Outlier Accuracy:", outlier_acc)

    # CLEAN
    X_clean, y_clean = dataX, dataY
    X_train_clean, X_test_clean, y_train_clean, y_test_clean = train_test_split(X_clean, y_clean, test_size=0.2, random_state=RANDOM_STATE)
    clean_acc = np.mean([knn(x, k, X_train_clean, y_train_clean) == y_test_clean[i] for i, x in enumerate(X_test_clean)])
    print(f"Clean Accuracy:", clean_acc)

    plt.show()

def test_outliers(upper=100):
    x_series, y_series = [], []
    dataX, dataY = make_blobs(n_samples=NUM_DATA, n_features=2, centers=2, cluster_std=2, random_state=RANDOM_STATE)
    for i in range(10, upper):
        outlierX, outlierY = np.random.uniform(low=-15, high=15, size=(NUM_OUTLIERS, 2)), np.random.choice([0, 1], size=NUM_OUTLIERS)
        X, y = np.vstack([dataX, outlierX]), np.hstack([dataY, outlierY])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
        a = np.mean([knn(x, k, X_train, y_train) == y_test[i] for i, x in enumerate(X_test)])
        x_series.append(i)
        y_series.append(a)
    print("Average accuracy:", np.mean(y_series))
    plt.scatter(x_series, y_series)
    plt.xlabel("Number of outliers")
    plt.ylabel("Accuracy")
    plt.show()

main()
# test_outliers()