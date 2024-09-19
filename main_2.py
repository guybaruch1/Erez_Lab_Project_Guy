import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


# Reduced graph size for testing
def create_small_coherence_graph(data, max_edges=10, threshold=None):
    G = nx.Graph()

    # Only using a subset of nodes for testing (e.g., first 10)
    electrodes = list(range(1, 11))  # Use the first 10 electrodes

    # Add electrodes as nodes
    G.add_nodes_from(electrodes)

    # Add only a few edges for testing
    edge_count = 0
    for i in range(1, len(electrodes)):
        for j in range(i + 1, len(electrodes)):
            coherence_value = data.iloc[0, j]  # Coherence value
            if (threshold is None or coherence_value > threshold) and edge_count < max_edges:
                G.add_edge(i, j, weight=coherence_value)
                edge_count += 1
            if edge_count >= max_edges:
                break
    return G


# Simple graph plot with circular layout
def plot_graph_simple(G, title='Graph Visualization'):
    plt.figure(figsize=(8, 6))

    # Circular layout for faster rendering
    pos = nx.circular_layout(G)

    # Draw the graph with node labels
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_color='black',
            edge_color='gray')

    # Optionally, draw edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.show()


# Load the data
file_path = "C:/Users/guygu/Desktop/לימודים/מוח/פרקטיקום/FC_matrix_by_frequncy_bands)/FC_matrix_by_frequncy_bands/flatten_sub_02_film_coherence.csv"
data = pd.read_csv(file_path)

# Create a small graph for testing (limit the number of edges and nodes)
small_graph_delta = create_small_coherence_graph(data.loc[data['Unnamed: 0'] == 'delta'], max_edges=10)

# Plot the small graph
plot_graph_simple(small_graph_delta, title='Small Delta Coherence Graph')
