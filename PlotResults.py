import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class PlotResults:
    def __init__(self, global_results, node_results):
        self.global_results = global_results
        self.node_results = node_results

    def plot_global_metric(self, metric_name):
        """
        Plots a bar graph showing the mean of a global metric for each subject across rest and film conditions.
        """
        rest_means = []
        film_means = []
        subjects = []

        # Collect mean values for each subject
        for wavelength in self.global_results:
            for subject in self.global_results[wavelength]:
                rest_mean = self.global_results[wavelength][metric_name]['rest']
                film_mean = self.global_results[wavelength][metric_name]['film']
                rest_means.append(rest_mean)
                film_means.append(film_mean)
                subjects.append(subject)

        # Create bar plot
        x = np.arange(len(subjects))  # Number of subjects
        width = 0.35  # Width of the bars

        fig, ax = plt.subplots()
        ax.bar(x - width/2, rest_means, width, label='Rest')
        ax.bar(x + width/2, film_means, width, label='Film')

        # Add labels, title, and legend
        ax.set_xlabel('Subjects')
        ax.set_ylabel(metric_name)
        ax.set_title(f'Mean {metric_name} Across Subjects')
        ax.set_xticks(x)
        ax.set_xticklabels(subjects)
        ax.legend()

        plt.show()

# Example usage
if __name__ == "__main__":
    plotter = PlotResults(global_results, node_results)
    plotter.plot_global_metric('modularity')  # Replace 'modularity' with the global metric of interest
