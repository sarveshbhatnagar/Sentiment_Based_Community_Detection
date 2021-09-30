import networkx as nx
import pickle
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
"""
labels = ["a", "b", "c", "d", "e"]
x = np.array([0, 1, 2, 3, 4])

fig, ax = plt.subplots()
line, = ax.plot(x, x, "ro")
mplcursors.cursor(ax).connect(
    "add", lambda sel: sel.annotation.set_text(labels[sel.target.index]))

plt.show()

"""
fig = pickle.load(open('./data/communities/nosleep/fig_res5.0.pickle', 'rb'))
print(fig)
plt.figure(fig.number)
plt.show()
fig.show()
print('a')
