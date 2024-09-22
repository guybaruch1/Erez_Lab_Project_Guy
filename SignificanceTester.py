from scipy import stats
import numpy as np
import pickle
from shared import Wavelength

class SignificanceTester:
    def __init__(self, metrics_file):
        """
        Initializes the SignificanceTester by loading the metrics file.
        """
        self.metrics = self.load_metrics(metrics_file)

    def load_metrics(self, filename):
        """
        Loads the calculated metrics from a Pickle file.
        """
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def extract_global_metric(self, metric_name, state=None, wavelength=None):
        """
        Extracts the global metric values for a given state and wavelength.
        """
        metric_values = []
        for (subject, task_state, task_wavelength), metrics in self.metrics.items():
            if (state is None or task_state == state) and (wavelength is None or task_wavelength == wavelength):
                metric_values.append(metrics['global_metrics'][metric_name])
        return np.array(metric_values)

    def extract_node_based_metric(self, metric_name, state=None, wavelength=None):
        """
        Extracts node-based metric values for a given state and wavelength.
        Returns all node-level values (not aggregated) for each graph.
        """
        metric_values = []
        for (subject, task_state, task_wavelength), metrics in self.metrics.items():
            if (state is None or task_state == state) and (wavelength is None or task_wavelength == wavelength):
                # Assuming node-based metric values are stored in a dictionary under 'node_metrics'
                metric_values.extend(metrics['node_metrics'][metric_name].values())  # Get all node-level values
        return np.array(metric_values)

    def perform_paired_t_test(self, metric_name, state_1, state_2, wavelength, alpha=0.05):
        """
        Performs a paired t-test on global metrics between two states for a specific wavelength.
        Returns the t-statistic, p-value, and whether the result is significant.
        """
        values_state_1 = self.extract_global_metric(metric_name, state_1, wavelength)
        values_state_2 = self.extract_global_metric(metric_name, state_2, wavelength)

        # Perform the paired t-test
        t_statistic, p_value = stats.ttest_rel(values_state_1, values_state_2)

        # Check if the result is significant
        is_significant = p_value < alpha

        return {
            't_statistic': t_statistic,
            'p_value': p_value,
            'significant': is_significant
        }

    def perform_ks_test(self, metric_name, state_1, state_2, wavelength, alpha=0.05):
        """
        Performs a Kolmogorov-Smirnov (K-S) test on node-level metrics to compare distributions.
        Returns the K-S statistic, p-value, and whether the result is significant.
        """
        values_state_1 = self.extract_node_based_metric(metric_name, state_1, wavelength)
        values_state_2 = self.extract_node_based_metric(metric_name, state_2, wavelength)

        # Perform the K-S test
        ks_statistic, p_value = stats.ks_2samp(values_state_1, values_state_2)

        # Check if the result is significant
        is_significant = p_value < alpha

        return {
            'ks_statistic': ks_statistic,
            'p_value': p_value,
            'significant': is_significant
        }

    def compare_global_metrics(self, state_1, state_2, alpha=0.05):
        """
        Compares all global metrics between two states using a paired t-test.
        """
        results = {}

        for wavelength in Wavelength:
            print(f"Comparing global metrics for Wavelength: {wavelength.name}")
            results[wavelength] = {}

            # Loop through all global metrics (e.g., num_nodes, modularity)
            for metric_name in next(iter(self.metrics.values()))['global_metrics'].keys():
                result = self.perform_paired_t_test(metric_name, state_1, state_2, wavelength, alpha)
                results[wavelength][metric_name] = result

                print(f"  Global Metric: {metric_name}")
                print(f"    t-statistic: {result['t_statistic']:.4f}, p-value: {result['p_value']:.4f}")
                if result['significant']:
                    print(f"    Result: Significant at alpha = {alpha}")
                else:
                    print(f"    Result: Not significant")
                print("-" * 40)

        return results

    def compare_node_metrics(self, state_1, state_2, alpha=0.05):
        """
        Compares all node-level metrics between two states using the Kolmogorov-Smirnov test.
        """
        results = {}

        for wavelength in Wavelength:
            print(f"Comparing node-level metrics for Wavelength: {wavelength.name}")
            results[wavelength] = {}

            # Loop through all node-based metrics (e.g., degree_centrality, clustering_coefficient)
            for metric_name in next(iter(self.metrics.values()))['node_metrics'].keys():
                result = self.perform_ks_test(metric_name, state_1, state_2, wavelength, alpha)
                results[wavelength][metric_name] = result

                print(f"  Node-Based Metric: {metric_name}")
                print(f"    K-S statistic: {result['ks_statistic']:.4f}, p-value: {result['p_value']:.4f}")
                if result['significant']:
                    print(f"    Result: Significant at alpha = {alpha}")
                else:
                    print(f"    Result: Not significant")
                print("-" * 40)

        return results

# Example usage of the class
if __name__ == "__main__":
    significance_tester = SignificanceTester('graph_metrics.pkl')

    # Compare global metrics using paired t-test
    print("\nComparing Global Metrics (Paired T-Test):")
    global_results = significance_tester.compare_global_metrics(state_1='rest', state_2='film', alpha=0.05)

    # Compare node-level metrics using K-S test
    print("\nComparing Node-Level Metrics (K-S Test):")
    node_results = significance_tester.compare_node_metrics(state_1='rest', state_2='film', alpha=0.05)
