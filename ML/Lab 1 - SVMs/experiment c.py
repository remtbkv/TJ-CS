import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split

def plot_svc_decision_function(model, ax=None):
    if ax is None:
        ax = plt.gca()
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    X, Y = np.meshgrid(np.linspace(xlim[0], xlim[1], 30), np.linspace(ylim[0], ylim[1], 30))
    P = model.decision_function(np.vstack([X.ravel(), Y.ravel()]).T).reshape(X.shape)
    ax.contour(X, Y, P, colors='k', levels=[-1, 0, 1], alpha=0.5, linestyles=['--', '-', '--'])
    
N=300
# normal
X, y = make_blobs(n_samples=N, centers=2, random_state=42, cluster_std=0.60)
# overlap, noise
# X, y = make_blobs(n_samples=N, centers=2, random_state=42, cluster_std=3)
# sparse
# X, y = make_blobs(n_samples=30, centers=2, random_state=42, cluster_std=4)

C_values = [0.01, 0.1, 1, 10, 100, 1000]

fig, ax = plt.subplots(2, 3, figsize=(15, 10))
ax = ax.ravel()

for i, C in enumerate(C_values):
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = SVC(kernel='linear', C=C)
    model.fit(x_train, y_train)
    ax = ax[i]
    ax.scatter(x_train[:, 0], x_train[:, 1], c=y_train, s=50, cmap='autumn')
    plot_svc_decision_function(model, ax)
    ax.set_title(f"C={C}, Margin={round(1/np.linalg.norm(model.coef_[0]),2)}")
    print(f"C={C}, Train Accuracy: {round(model.score(x_train, y_train),3)}, Test Accuracy: {round(model.score(x_test, y_test),3)}")

plt.tight_layout()
plt.show()