import numpy as np
from neighborfinder import NeighborFinder
import pandas as pd

data = np.array(pd.read_csv('../../data/anomaly.csv', skip_blank_lines=True, header=None))

# use our own kd-tree implementation
neighbor_finder = NeighborFinder(data, 'mykdtree')

n_neighbors = 10

nr, nc = data.shape
distances = np.zeros(nr)
index = 0
total_time = 0
for i in range(nr):
    distance_to_neighbors, query_time = neighbor_finder.find_neighbors(data[i, :], n_neighbors)
    distances[i] = np.mean(distance_to_neighbors)
    total_time += query_time

is_anomaly_knn = distances > 0.5
size = 1000 * distances ** 2

print('found {} anomalies, total query time = {:.5f}s'.format(is_anomaly_knn.sum(), total_time))
