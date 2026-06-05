import pickle
from matplotlib import pyplot as plt

L = 0.0001

def load_saved_info():
    with open(f"saved_info_{L}", "rb") as f:
        return pickle.load(f)

# epoch, misclassified, accuracy, error, weight_val, gradient_error, w, b
lst = load_saved_info()
epoch_accuracy = [(i[0], i[2]) for i in lst]
epoch_error = [(i[0], i[3]) for i in lst]
weightval_error = [(i[4], i[3]) for i in lst]

graphs = [epoch_accuracy, epoch_error, weightval_error]
titles = ["Epoch vs Accuracy", "Epoch vs Error", "Weight Value vs Error"]
x_labels = ["Epoch", "Epoch", "Weight Value"]
y_labels = ["Accuracy%", "Error%", "Error%"]

for i in range(3):
    x, y = zip(*graphs[i])
    plt.plot(x,y)
    
    # for purely vertical lines
    # i =2
    # x_only = -0.0011187105761916024
    # e_max = 91.08
    # plt.vlines(x=x_only, ymin=0, ymax=e_max)
    # plt.xticks([x])
    
    plt.title(titles[i])
    plt.xlabel(x_labels[i])
    plt.ylabel(y_labels[i])
    plt.show()