import numpy as np
import networkx as nx
import community
import gudhi
import scipy.io
from sklearn import preprocessing
import itertools
import seaborn as sns
import matplotlib.pyplot as plt

G = nx.petersen_graph()
subax1 = plt.subplot(121)
nx.draw(G, with_labels=True)
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
clustering = nx.clustering(G)
global_clustering = nx.average_clustering(G)
plt.show()
print(clustering, global_clustering)


# Generate a small-world network using the Watts-Strogatz model
n = 10  # Number of nodes
k = 4   # Number of neighbors for each node
p = 0.3  # Probability of rewiring

G = nx.watts_strogatz_graph(n, k, p)

subax1 = plt.subplot(121)
nx.draw(G, with_labels=True)
subax2 = plt.subplot(122)
nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

clustering = nx.clustering(G)
global_clustering = nx.average_clustering(G)

plt.show()
print(clustering, global_clustering)