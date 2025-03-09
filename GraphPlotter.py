import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class GraphPlotter:
    def __init__(self, metrics_file):
        """
        Initializes the GraphPlotter class by loading the metrics file.
        """
        self.metrics = self.load_metrics(metrics_file)

    def load_metrics(self, filename):
        """
        Loads the calculated metrics from a Pickle file.
        """
        with open(filename, 'rb') as file:
            metrics = pickle.load(file)

        # # Debugging: Print keys in metrics to ensure all subjects are there
        # print("Loaded Metrics Keys: ", metrics.keys())

        return metrics

    def extract_global_metric(self, metric_name):
        """
        Extracts the global metric values (GCC in this case) for each wavelength and state.
        """
        data = []

        # Loop through all subjects and extract the global metric (GCC) for rest and film states
        for (subject, state, wavelength), metrics in self.metrics.items():
            # # Debugging: Print subject, state, and wavelength to check iteration
            # print(f"Subject: {subject}, State: {state}, Wavelength: {wavelength.name}")

            if metric_name in metrics['global_metrics']:
                data.append({
                    'Subject': subject,
                    'State': state,
                    'Wavelength': wavelength.name,
                    'GCC': metrics['global_metrics'][metric_name]
                })

        # Convert the collected data into a pandas DataFrame
        return pd.DataFrame(data)

    def extract_node_gcc(self):
        """
        Extracts node-based GCC values for each wavelength and state.
        """
        data = []

        # Loop through all subjects and extract node-level GCC for rest and film states
        for (subject, state, wavelength), metrics in self.metrics.items():
            if 'clustering_coefficient' in metrics['node_metrics']:
                # Get node-level GCC values and add them to the data list
                for node, gcc_value in metrics['node_metrics']['clustering_coefficient'].items():
                    data.append({
                        'Subject': subject,
                        'State': state,
                        'Wavelength': wavelength.name,
                        'Node': node,
                        'Node_GCC': gcc_value
                    })

        # Convert the collected data into a pandas DataFrame
        return pd.DataFrame(data)

    def calculate_mean_gcc(self, df):
        """
        Groups the data by Wavelength and State, then calculates the mean GCC.
        """
        return df.groupby(['Wavelength', 'State'])['GCC'].mean().reset_index()

    def calculate_mean_node_gcc(self):
        """
        Extracts node-based GCC values and calculates the mean for each wavelength and state.
        """
        data = []

        # Loop through all subjects and extract node-level GCC for rest and film states
        for (subject, state, wavelength), metrics in self.metrics.items():
            if 'clustering_coefficient' in metrics['node_metrics']:
                # Get node-level GCC values and calculate the mean for this subject, wavelength, and state
                node_gcc_values = list(metrics['node_metrics']['clustering_coefficient'].values())
                mean_gcc = np.mean(node_gcc_values)

                # Append the mean GCC value to the data list
                data.append({
                    'Wavelength': wavelength.name,
                    'State': state,
                    'Mean_Node_GCC': mean_gcc
                })

        # Convert the collected data into a pandas DataFrame
        return pd.DataFrame(data)

    def plot_gcc_histogram(self, mean_gcc_df):
        """
        Plots a histogram to compare the mean GCC values for rest and film across wavelengths.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(data=mean_gcc_df, x='Wavelength', y='GCC', hue='State')
        plt.title("Mean Global Clustering Coefficient by Wavelength and State")
        plt.ylabel("Mean GCC")
        plt.tight_layout()
        plt.show()

    def plot_node_gcc_distribution(self, df):
        """
        Plots the distribution of node-based GCC for each wavelength, overlaid by state.
        """
        plt.figure(figsize=(12, 8))

        # Loop through each wavelength and create a subplot for it
        wavelengths = df['Wavelength'].unique()
        for i, wavelength in enumerate(wavelengths, 1):
            plt.subplot(2, 3, i)  # Assuming 6 wavelengths (2 rows, 3 columns)

            # Plot distribution for the given wavelength, split by state, with overlay
            sns.kdeplot(data=df[df['Wavelength'] == wavelength], x='Node_GCC', hue='State', fill=True,
                        common_norm=False, palette="Set1", alpha=0.5)

            plt.title(f"Node GCC Distribution - {wavelength}")
            plt.xlabel("Node GCC")
            plt.ylabel("Density")

        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    graph_plotter = GraphPlotter('graph_metrics.pkl')
    df = graph_plotter.extract_global_metric('global_clustering_coefficient')
    mean_gcc_df = graph_plotter.calculate_mean_gcc(df)
    graph_plotter.plot_gcc_histogram(mean_gcc_df)
    # print(mean_gcc_df)
    # Extract node-based GCC values
    df = graph_plotter.extract_node_gcc()

    # Plot the distribution of node-based GCC for each wavelength and state
    graph_plotter.plot_node_gcc_distribution(df)