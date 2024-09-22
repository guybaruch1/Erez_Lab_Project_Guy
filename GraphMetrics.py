import networkx as nx
import pickle
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
        Registers all global and node-level metric functions in a dictionary.
        """
        metrics = {
            'num_nodes': self.num_nodes,
            'num_edges': self.num_edges,
            'degree_centrality': self.degree_centrality,
            'clustering_coefficient': self.clustering_coefficient,
            'modularity': self.modularity,
            'global_clustering_coefficient': self.global_clustering_coefficient
        }
        return metrics

    def num_nodes(self, graph):
        """
        Returns the number of nodes (global metric).
        """
        return graph.number_of_nodes()

    def num_edges(self, graph):
        """
        Returns the number of edges (global metric).
        """
        return graph.number_of_edges()

    def degree_centrality(self, graph):
        """
        Returns both global and node-level degree centrality.
        - Global: Average degree centrality.
        - Node-level: Degree centrality for each node.
        """
        degree_centrality = nx.degree_centrality(graph)
        global_degree_centrality = sum(degree_centrality.values()) / len(degree_centrality)  # Global value
        return {
            'global': global_degree_centrality,
            'node': degree_centrality  # Node-level values
        }

    def clustering_coefficient(self, graph):
        """
        Returns both global and node-level clustering coefficient.
        - Global: Average clustering coefficient.
        - Node-level: Clustering coefficient for each node.
        """
        clustering_coeffs = nx.clustering(graph)
        global_clustering_coefficient = sum(clustering_coeffs.values()) / len(clustering_coeffs)  # Global value
        return {
            'global': global_clustering_coefficient,
            'node': clustering_coeffs  # Node-level values
        }

    def modularity(self, graph):
        """
        Returns the modularity of the graph using the Louvain method (global metric).
        """
        import community  # Louvain method for modularity
        partition = community.best_partition(graph)
        return community.modularity(partition, graph)

    def global_clustering_coefficient(self, graph):
        """
        Returns the global clustering coefficient (transitivity) for the graph.
        """
        return nx.transitivity(graph)

    def calculate_metrics_for_graph(self, graph):
        """
        Iterates through the registered metrics and calculates both global and node-level metrics for a given graph.
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
        Iterates over all graphs, calculates metrics (both global and node-level), stores them in a dictionary,
        and prints the results to the terminal.
        """
        all_metrics = {}
        for key, graph_file in self.metadata.items():
            # Load the graph from the GraphML file
            graph = nx.read_graphml(graph_file)
            subject, state, wavelength = key

            print(f"\nProcessing graph for Subject: {subject}, State: {state}, Wavelength: {wavelength.name}")

            # Calculate metrics for this graph
            metrics = self.calculate_metrics_for_graph(graph)

            # Print global and node-level metrics
            for metric_name, metric_values in metrics.items():
                if isinstance(metric_values, dict) and 'global' in metric_values:
                    print(f"  Metric: {metric_name}")
                    print(f"    Global value: {metric_values['global']}")
                    print(f"    Node-level values: {metric_values['node']}")
                else:
                    print(f"  Metric: {metric_name}: {metric_values}")

            # Store the metrics with a unique identifier (e.g., subject, state, wavelength)
            all_metrics[key] = metrics

        # Save the calculated metrics to a .pkl file
        with open('graph_metrics.pkl', 'wb') as file:
            pickle.dump(all_metrics, file)

        print("\nMetrics saved to 'graph_metrics.pkl'")

# Example usage of the class
if __name__ == "__main__":
    # Initialize the class with the metadata file
    graph_metrics = GraphMetrics('graph_metadata.pkl')

    # Calculate metrics and print them to the terminal
    all_metrics = graph_metrics.iterate_and_calculate_metrics()
