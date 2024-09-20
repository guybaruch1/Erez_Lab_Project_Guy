import pickle
import networkx as nx
import numpy as np
from shared import Wavelength

class GraphMetrics:
    def __init__(self, metadata_file):
        """
        Initializes the GraphMetrics class by loading the metadata and defining metric functions.
        """
        self.metadata = self.load_metadata(metadata_file)
        self.metrics_registry = self.register_metrics()

    def load_metadata(self, filename):
        """
        Loads metadata from a Pickle file.
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def register_metrics(self):
        """
        Registers all metric functions in a dictionary for easy management.
        """
        metrics = {
            'num_nodes': self.num_nodes,
            'num_edges': self.num_edges,
            'average_clustering': self.average_clustering,
            'graph_density': self.graph_density,
            'degree_centrality': self.degree_centrality,
            'average_shortest_path': self.average_shortest_path_length,
            # Add more metrics here as needed
        }
        return metrics

    def num_nodes(self, graph):
        return graph.number_of_nodes()

    def num_edges(self, graph):
        return graph.number_of_edges()

    def average_clustering(self, graph):
        return nx.average_clustering(graph)

    def graph_density(self, graph):
        return nx.density(graph)

    def degree_centrality(self, graph):
        return np.mean(list(nx.degree_centrality(graph).values()))

    def average_shortest_path_length(self, graph):
        if nx.is_connected(graph):
            return nx.average_shortest_path_length(graph)
        return float('inf')  # Return infinity for disconnected graphs

    def calculate_metrics_for_graph(self, graph):
        """
        Iterates through the registered metrics and calculates them for a given graph.
        """
        results = {}
        for metric_name, metric_func in self.metrics_registry.items():
            try:
                results[metric_name] = metric_func(graph)
            except Exception as e:
                results[metric_name] = f"Error: {e}"
        return results

    def iterate_and_calculate_metrics(self):
        """
        Iterates over all graphs, calculates metrics, and stores them in a dictionary.
        """
        all_metrics = {}
        for key, graph_file in self.metadata.items():
            # Load the graph from the GraphML file
            graph = nx.read_graphml(graph_file)
            subject, state, wavelength = key

            # Calculate all metrics for the current graph
            metrics = self.calculate_metrics_for_graph(graph)

            # Store the metrics with a unique identifier (e.g., subject, state, wavelength)
            all_metrics[key] = metrics

            print(f"Metrics for {subject}, {state}, {wavelength.name}: {metrics}")
            print("-" * 40)

        return all_metrics


# Example usage of the class
if __name__ == "__main__":
    # Initialize the class with the metadata file
    graph_metrics = GraphMetrics('graph_metadata.pkl')

    # Iterate over all graphs and calculate metrics
    all_metrics = graph_metrics.iterate_and_calculate_metrics()
