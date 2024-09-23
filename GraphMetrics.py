import networkx as nx
import pickle
from shared import Wavelength

class GraphMetrics:
    def __init__(self, metadata_file):
        """
        Initializes the GraphMetrics class by loading the metadata and defining metric functions.
        """
        self.metadata = self.load_metadata(metadata_file)
        self.global_metrics_registry = self.register_global_metrics()
        self.node_metrics_registry = self.register_node_metrics()

    def load_metadata(self, filename):
        """
        Loads metadata from a Pickle file.
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def register_global_metrics(self):
        """
        Registers global graph-level metric functions.
        """
        global_metrics = {
            'modularity': self.modularity,
            'global_clustering_coefficient': self.global_clustering_coefficient,
        }
        return global_metrics

    def register_node_metrics(self):
        """
        Registers node-level metric functions (for each node).
        """
        node_metrics = {
            'degree_centrality': self.node_degree_centrality,
            'clustering_coefficient': self.node_clustering_coefficient,
        }
        return node_metrics

    def num_nodes(self, graph):
        """
        Calculates the number of nodes (global metric).
        """
        return graph.number_of_nodes()

    def num_edges(self, graph):
        """
        Calculates the number of edges (global metric).
        """
        return graph.number_of_edges()

    def modularity(self, graph):
        """
        Calculates the modularity of the graph (global metric).
        """
        import community
        partition = community.best_partition(graph)
        return community.modularity(partition, graph)

    def global_clustering_coefficient(self, graph):
        """
        Calculates the global clustering coefficient (transitivity) (global metric).
        """
        return nx.transitivity(graph)

    def node_degree_centrality(self, graph):
        """
        Calculates degree centrality for each node (node-level metric).
        """
        return nx.degree_centrality(graph)

    def node_clustering_coefficient(self, graph):
        """
        Calculates local clustering coefficient for each node (node-level metric).
        """
        return nx.clustering(graph)

    def calculate_global_metrics(self, graph):
        """
        Iterates through the registered global metrics and calculates them for a given graph.
        """
        results = {}
        for metric_name, metric_func in self.global_metrics_registry.items():
            try:
                results[metric_name] = metric_func(graph)
            except Exception as e:
                results[metric_name] = f"Error: {e}"
        return results

    def calculate_node_metrics(self, graph):
        """
        Iterates through the registered node-level metrics and calculates them for each node in the graph.
        """
        results = {}
        for metric_name, metric_func in self.node_metrics_registry.items():
            try:
                results[metric_name] = metric_func(graph)
            except Exception as e:
                results[metric_name] = f"Error: {e}"
        return results

    def iterate_and_calculate_metrics(self):
        """
        Iterates over all graphs, calculates both global and node-level metrics, prints results,
        and stores them in a dictionary.
        """
        all_metrics = {}

        for key, graph_file in self.metadata.items():
            # Load the graph from the GraphML file
            graph = nx.read_graphml(graph_file)

            # Unpack the key
            subject, state, wavelength = key

            print(f"Calculating metrics for Subject: {subject}, State: {state}, Wavelength: {wavelength.name}")

            # Calculate global metrics
            global_metrics = self.calculate_global_metrics(graph)
            print("\nGlobal Metrics:")
            for metric_name, value in global_metrics.items():
                print(f"  {metric_name}: {value}")

            # Calculate node-level metrics
            node_metrics = self.calculate_node_metrics(graph)
            print("\nNode-Level Metrics:")
            for metric_name, node_values in node_metrics.items():
                values_array = [f"{value:.4f}" for node, value in node_values.items()]
                print(f"  {metric_name}: [{', '.join(values_array)}]")

            # Store both global and node-level metrics in the dictionary
            all_metrics[key] = {
                'global_metrics': global_metrics,
                'node_metrics': node_metrics
            }

        # Save the calculated metrics to a .pkl file
        with open('graph_metrics.pkl', 'wb') as file:
            pickle.dump(all_metrics, file)

        print("\nMetrics saved to 'graph_metrics.pkl'")


if __name__ == "__main__":
    graph_metrics = GraphMetrics('graph_metadata.pkl')

    # Calculate and print metrics
    all_metrics = graph_metrics.iterate_and_calculate_metrics()
