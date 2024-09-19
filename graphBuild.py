import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# the stop value in the matrix
STOP = 1.0

# the start of the matrix
START = 2

# the top present
TOP = 0.1


# import community
# import gudhi
from scipy import stats
# from sklearn import preprocessing
# import itertools
# import seaborn as sns


def build_graph_from_csv(csv_file):
    # Create a graph
    G = nx.Graph()

    # Read CSV file and add nodes and edges to the graph
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        # row will be the second row
        row = next(reader)

        k = START  # the column number

        # init the graph
        edge = float(row[k])
        for num_node in range(1, 1000):
            if edge == 1:
                break
            G.add_node(num_node)
            k = k + 1
            edge = float(row[k])

        # add the edges
        k = START
        for i in range(1, num_node):

            # end of the row
            if k == len(row):
                break

            for j in range(i + 1, num_node + 2):
                edge = float(row[k])

                # end of the i column in the matrix
                if edge == STOP:
                    k = k + 1
                    break

                # add the edge
                G.add_edge(i, j, weight=float(edge))
                k = k + 1
    return G


def threshold(G):
    # sort the edges
    sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    # number of edges to keep
    num_edges_to_keep = int(len(sorted_edges) * TOP)
    # take the top (TOP)% the largest edges
    top_edges = sorted_edges[:num_edges_to_keep]
    # create the new graph with only the top edges
    G_top = nx.Graph()

    for edge in top_edges:
        G_top.add_node(edge[0])
        G_top.add_node(edge[1])
    G_top.add_edges_from(top_edges)
    return G_top

