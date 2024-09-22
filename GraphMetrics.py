import pickle
import networkx as nx
import numpy as np
import community  # For modularity
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
            'degree_centrality': self.degree_centrality,
            'clustering_coefficient': self.clustering_coefficient,
            'modularity': self.modularity,
            'global_clustering_coefficient': self.global_clustering_coefficient,
            # We can add more metrics here as needed...
        }
        return metrics

    def num_nodes(self, graph):
        return graph.number_of_nodes()

    def num_edges(self, graph):
        return graph.number_of_edges()

    def degree_centrality(self, graph):
        degree_centrality = nx.degree_centrality(graph)
        return np.mean(list(degree_centrality.values()))  # Return the average degree centrality

    def clustering_coefficient(self, graph):
        clustering_coeffs = nx.clustering(graph)
        return np.mean(list(clustering_coeffs.values()))  # Return the average clustering coefficient

    def modularity(self, graph):
        """
        Calculates the modularity using the Louvain method for community detection.
        """
        if len(graph.nodes()) == 0:  # Empty graph case
            return None
        partition = community.best_partition(graph)  # Louvain algorithm
        return community.modularity(partition, graph)

    def global_clustering_coefficient(self, graph):
        """
        Calculates the global clustering coefficient (transitivity) of the graph.
        """
        return nx.transitivity(graph)

    def average_clustering(self, graph):
        return nx.average_clustering(graph)

    def graph_density(self, graph):
        return nx.density(graph)

    # def degree_centrality(self, graph):
    #     return np.mean(list(nx.degree_centrality(graph).values()))


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

            # Save the calculated metrics to a .pkl file
            with open('graph_metrics.pkl', 'wb') as file:
                pickle.dump(all_metrics, file)

            print("Metrics saved to 'graph_metrics.pkl'")

        return all_metrics


# Example usage of the class
if __name__ == "__main__":
    # Initialize the class with the metadata file
    graph_metrics = GraphMetrics('graph_metadata.pkl')

    # Iterate over all graphs and calculate metrics
    all_metrics = graph_metrics.iterate_and_calculate_metrics()
