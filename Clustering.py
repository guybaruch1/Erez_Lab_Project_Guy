import numpy as np
import networkx as nx
import community
import gudhi
import scipy.io
from sklearn import preprocessing
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
import csv
import os
import statistics

file_path = "C:/Users/guygu/Desktop/לימודים/מוח/פרקטיקום/FC_matrix_by_frequncy_bands)/FC_matrix_by_frequncy_bands/flatten_sub_02_film_coherence.csv"


def mean_calc(file_path):
    # Read the values from the CSV file and calculate the mean
    values = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip the header row if it exists
        next(csv_reader, None)

        i = 2
        for row in csv_reader:
            for value in row[i:]:
                try:
                    numeric_value = float(value)
                    values.append(numeric_value)
                except ValueError:
                    pass
            i = i + 1

    # Calculate the mean of the values
    mean_value = statistics.mean(values)
    print(f"Mean value: {mean_value}")

    return mean_value


mean_calc(file_path)