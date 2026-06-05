import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split

def draw(fit_model, x, y, iris=False):
    plt.figure(figsize=(8, 6))
    ax = plt.gca()
    scatter = ax.scatter(x[:, 0], x[:, 1], c=y, s=50, cmap='viridis', edgecolor='k')
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    x_grid, y_grid = np.meshgrid(np.linspace(xlim[0], xlim[1], 1000), np.linspace(ylim[0], ylim[1], 1000))
    P = fit_model.predict(np.column_stack((x_grid.ravel(), y_grid.ravel()))).reshape(x_grid.shape)
    plt.contour(x_grid, y_grid, P, colors='k')
    plt.contourf(x_grid, y_grid, P, alpha=0.3, cmap='viridis')
    if iris:
        legend_labels = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
        handles, _ = scatter.legend_elements()
        ax.legend(handles, [legend_labels[i] for i in range(3)], title="Classes")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    plt.show()

def plot_svm(n=100, N=200, ax=None):
    X, y = make_blobs(n_samples=N, centers=2, random_state=42, cluster_std=0.60)
    X, y = X[:n], y[:n]
    model = SVC(kernel='linear', C=1E10)
    model.fit(X, y)
    draw(model, X, y)

def iris(C=1):
    iris = pd.read_csv("iris_2.csv")
    X = iris.iloc[:, :-1].values
    y = np.array([0 if i == 'Iris-setosa' else 1 if i == 'Iris-versicolor' else 2 for i in iris.iloc[:, -1]])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = SVC(kernel='linear', C=C)
    model.fit(X_train, y_train)
    draw(model, X_train, y_train, iris=True)

iris()