import csv
import networkx as nx
import os
from enum import Enum
import pickle


class Wavelength(Enum):
    DELTA = 1  # 1-4 Hz
    THETA = 2  # 4-8 Hz
    ALPHA = 3  # 8-12 Hz
    BETA = 4  # 12-30 Hz
    GAMMA = 5  # 30-100 Hz
    HIGH_GAMMA = 6  # 100+ Hz


# Constants
STOP = 1.0
START = 2
TOP = 0.1

# Define subjects, states, and a dictionary to hold the graph file paths
subjects = {"03", "06", "07", "10", "13", "14", "16", "17", "18", "19", "20", "22", "24", "26", "27", "28",
            "31", "37", "38", "40", "41", "43", "45", "46", "48", "49", "50", "54", "55", "60", "63"}
states = {"rest", "film"}
graphml_directory = "saved_graphml_files"
metadata_map = {}  # Dictionary to hold graph file paths with key (subject, state, wavelength)

# Ensure the GraphML directory exists
os.makedirs(graphml_directory, exist_ok=True)

# Base CSV file address
csv_address_base = "C:/Users/guygu/Desktop/לימודים/מוח/פרקטיקום/FC_matrix_by_frequncy_bands" \
                   ")/FC_matrix_by_frequncy_bands/flatten_sub_"


def build_graph_from_row(row, start=START, stop=STOP):
    """
    Builds a graph from a single row of data.
    """
    G = nx.Graph()
    k = start
    edge = float(row[k])

    # Add nodes
    for num_node in range(1, 1000):
        if edge == stop:
            break
        G.add_node(num_node)
        k += 1
        if k < len(row):
            edge = float(row[k])
        else:
            break

    # Add edges
    k = start
    for i in range(1, num_node):
        if k >= len(row):
            break

        for j in range(i + 1, num_node + 2):
            edge = float(row[k])
            if edge == stop:
                k += 1
                break
            G.add_edge(i, j, weight=edge)
            k += 1
    return G


def threshold(G, top=TOP):
    """Threshold the graph by keeping only the top percentage of edges."""
    sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
    num_edges_to_keep = int(len(sorted_edges) * top)
    top_edges = sorted_edges[:num_edges_to_keep]

    G_top = nx.Graph()
    for edge in top_edges:
        G_top.add_node(edge[0])
        G_top.add_node(edge[1])
    G_top.add_edges_from(top_edges)

    return G_top


def build_graphs_from_csv(csv_file, start=START, stop=STOP):
    """
    Builds a list of graphs, one per row in the CSV file.
    Each row corresponds to a different wavelength.
    """
    graphs = []

    # Read CSV file and build graphs for each row
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        # Process each row and treat it as a graph corresponding to a wavelength
        for row in reader:
            graph = build_graph_from_row(row, start, stop)
            graph_top = threshold(graph)
            graphs.append(graph_top)

    return graphs


def save_graph_to_graphml(graph, filename):
    """Saves a graph to a GraphML file."""
    nx.write_graphml(graph, filename)


def save_metadata(metadata, filename='graph_metadata.pkl'):
    """Saves metadata to a file using Pickle."""
    with open(filename, 'wb') as file:
        pickle.dump(metadata, file)


def load_metadata(filename='graph_metadata.pkl'):
    """Loads metadata from a Pickle file."""
    with open(filename, 'rb') as file:
        return pickle.load(file)


def save_graphs(subjects, states, csv_address_base, graphml_directory):
    """
    Loops through each subject and state, builds graphs from CSV,
    and saves them to GraphML files. Metadata is stored in a dictionary.
    """
    for subject in subjects:
        for state in states:
            # Construct CSV filename for each subject and state
            csv_file = f"{csv_address_base}{subject}_{state}_coherence.csv"
            graphs = build_graphs_from_csv(csv_file)

            # Store each graph by its wavelength in the metadata map
            for wavelength_enum, graph in zip(Wavelength, graphs):
                # Create a unique filename for each graph
                graphml_filename = f"{graphml_directory}/graph_{subject}_{state}_{wavelength_enum.name}.graphml"
                save_graph_to_graphml(graph, graphml_filename)

                # Store the file path in the metadata map
                key = (subject, state, wavelength_enum)
                metadata_map[key] = graphml_filename

    # Save the metadata map
    save_metadata(metadata_map)


# Example usage: Save the graphs for each subject, state, and wavelength to GraphML files
save_graphs(subjects, states, csv_address_base, graphml_directory)