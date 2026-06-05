from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np


def knn(x, k, X, Y):
    def ed(a, b): return np.sum(np.square(a - b))
    dist = [ed(x, x_train) for x_train in X]
    labels = [Y[i] for i in np.argsort(dist)[:k]]
    return np.argmax(np.bincount(labels))


RANDOM_STATE = 42
K = 22
# Imbalanced overlap
X, y = make_blobs(n_samples=[100, 5000], n_features=2, centers=[[-7, -7], [0, 0]], cluster_std=[4, 2], random_state=RANDOM_STATE)

# Balanced overlap
# X, y = make_blobs(n_samples=[1000, 1000], n_features=2, centers=[[-7, -7], [0, 0]], cluster_std=[4, 2], random_state=RANDOM_STATE)

# Imbalanced separate
# X, y = make_blobs(n_samples=[100, 5000], n_features=2, centers=[[-7, -7], [0, 0]], cluster_std=[0.5, 0.5], random_state=RANDOM_STATE)

# Balanced separate
# X, y = make_blobs(n_samples=[1000, 1000], n_features=2, centers=[[-7, -7], [0, 0]], cluster_std=[0.5, 0.5], random_state=RANDOM_STATE)

zero, one = X[y == 0], X[y == 1]
plt.scatter(zero[:, 0], zero[:, 1], color='blue', label='Label 0')
plt.scatter(one[:, 0], one[:, 1], color='orange', label='Label 1')
plt.legend()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
acc = np.mean([knn(x, K, X_train, y_train) == y_test[i] for i, x in enumerate(X_test)])
print(acc)

plt.show()
