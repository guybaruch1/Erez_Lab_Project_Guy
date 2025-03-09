import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
import pickle

from PlotResults import PlotResults
from SignificanceTester import SignificanceTester
from shared import Wavelength

# Assuming SignificanceTester and PlotResults are defined earlier or imported

class Main:
    def __init__(self, metrics_file):
        """
        Initializes the Main class by loading the metrics and setting up the SignificanceTester and PlotResults.
        """
        self.metrics_file = metrics_file
        self.significance_tester = SignificanceTester(metrics_file)
        self.global_results = None
        self.node_results = None
        self.plotter = None

    def run_significance_tests(self):
        """
        Run significance tests for global and node-level metrics.
        """
        print("\nRunning Global Metric Significance Tests (Paired T-Test):")
        self.global_results = self.significance_tester.compare_global_metrics(state_1='rest', state_2='film', alpha=0.05)

        print("\nRunning Node-Level Metric Significance Tests (K-S Test):")
        self.node_results = self.significance_tester.compare_node_metrics(state_1='rest', state_2='film', alpha=0.05)

    def initiate_plotting(self):
        """
        Initiates the PlotResults class after running significance tests.
        """
        self.plotter = PlotResults(self.global_results, self.node_results)

    def plot_global_metric(self, metric_name):
        """
        Plots the specified global metric using a bar plot.
        """
        if self.plotter is None:
            print("Please initiate plotting after running the significance tests.")
        else:
            self.plotter.plot_global_metric(metric_name)

    def plot_node_metric_histogram(self, metric_name, wavelength):
        """
        Plots the distribution of the specified node-level metric using a histogram and KDE.
        """
        if self.plotter is None:
            print("Please initiate plotting after running the significance tests.")
        else:
            self.plotter.plot_node_metric_histogram(metric_name, wavelength)

    def plot_cluster_scatter(self, metric_name, wavelength):
        """
        Plots the cluster scatter plot for the specified node-level metric.
        """
        if self.plotter is None:
            print("Please initiate plotting after running the significance tests.")
        else:
            self.plotter.plot_cluster_scatter(metric_name, wavelength)

# Example usage
if __name__ == "__main__":
    # Initialize the main class
    main_app = Main('graph_metrics.pkl')

    # Run significance tests
    main_app.run_significance_tests()

    # Initiate plotting
    main_app.initiate_plotting()

    # Plot a global metric (replace 'modularity' with any global metric of your choice)
    main_app.plot_global_metric('modularity')

    # Plot a node-level metric histogram (replace 'degree_centrality' and Wavelength.DELTA with your values)
    main_app.plot_node_metric_histogram('degree_centrality', Wavelength.DELTA)
