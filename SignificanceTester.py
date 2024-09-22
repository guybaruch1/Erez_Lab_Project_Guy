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

    def extract_metric(self, metric_name, state=None, wavelength=None):
        """
        Extracts a specific metric for a given state and wavelength.
        If no state or wavelength is specified, returns the metric for all combinations.
        """
        metric_values = []
        for (subject, task_state, task_wavelength), metrics in self.metrics.items():
            if (state is None or task_state == state) and (wavelength is None or task_wavelength == wavelength):
                metric_values.append(metrics[metric_name])
        return np.array(metric_values)

    def perform_paired_t_test(self, metric_name, state_1, state_2, wavelength, alpha=0.05):
        """
        Performs a paired t-test between two states for a specific metric and wavelength.
        Returns the t-statistic, p-value, and whether the result is significant.
        """
        values_state_1 = self.extract_metric(metric_name, state_1, wavelength)
        values_state_2 = self.extract_metric(metric_name, state_2, wavelength)

        # Perform the paired t-test
        t_statistic, p_value = stats.ttest_rel(values_state_1, values_state_2)

        # Check if the result is significant
        is_significant = p_value < alpha

        return {
            't_statistic': t_statistic,
            'p_value': p_value,
            'significant': is_significant
        }

    def compare_metrics(self, state_1, state_2, alpha=0.05):
        """
        Compares all metrics between two states for each wavelength and performs a paired t-test.
        """
        results = {}

        # Loop through all wavelengths
        for wavelength in Wavelength:
            print(f"Comparing for Wavelength: {wavelength.name}")
            results[wavelength] = {}

            # Loop through all metrics
            for metric_name in next(iter(self.metrics.values())).keys():
                result = self.perform_paired_t_test(metric_name, state_1, state_2, wavelength, alpha)
                results[wavelength][metric_name] = result

                print(f"  Metric: {metric_name}")
                print(f"    t-statistic: {result['t_statistic']:.4f}, p-value: {result['p_value']:.4f}")
                if result['significant']:
                    print(f"    Result: Significant at alpha = {alpha}")
                else:
                    print(f"    Result: Not significant")
                print("-" * 40)

        return results


# Example usage of the class
if __name__ == "__main__":
    # Initialize the class with the metrics file
    significance_tester = SignificanceTester('graph_metrics.pkl')

    # Compare metrics between 'rest' and 'film' states for each wavelength using paired t-test
    results = significance_tester.compare_metrics(state_1='rest', state_2='film', alpha=0.05)
