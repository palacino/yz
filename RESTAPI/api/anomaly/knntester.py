import numpy as np

import pandas as pd
from api.anomaly.knnanomalydetector import KNNAnomalyDetector

ref_file_path = '../../data/anomaly.csv'
data = np.array(pd.read_csv(ref_file_path, skip_blank_lines=True, header=None))

# use our own kd-tree implementation
# neighbor_finder = NeighborFinder(data, 'mykdtree')

n_neighbors = 5

# nr, nc = data.shape
# distances = np.zeros(nr)
# index = 0
# total_time = 0
# for i in range(nr):
#     distance_to_neighbors, query_time = neighbor_finder.find_neighbors(data[i, :], n_neighbors)
#     distances[i] = np.mean(distance_to_neighbors)
#     total_time += query_time
#
# is_anomaly_knn = distances > 0.5
# size = 1000 * distances ** 2
#
# print('found {} anomalies, total query time = {:.5f}s'.format(is_anomaly_knn.sum(), total_time))

point = [3.0, 2.5]
anomaly_detector = KNNAnomalyDetector(ref_file_path, search_type='kdtree')
is_anomaly, score, message, query_time = anomaly_detector.detect_anomaly(point, n_neighbors=n_neighbors)

print('scipy   : point {}: is_anomaly={}, score={}, message={}, query time={:.5f}s'.format(point, is_anomaly, score, message,
                                                                                 query_time))

anomaly_detector = KNNAnomalyDetector(ref_file_path, search_type='mykdtree')
is_anomaly, score, message, query_time = anomaly_detector.detect_anomaly(point, n_neighbors=n_neighbors)

print('mykdtree: point {}: is_anomaly={}, score={}, message={}, query time={:.5f}s'.format(point, is_anomaly, score, message,
                                                                                 query_time))

anomaly_detector = KNNAnomalyDetector(ref_file_path, search_type='brute-force')
is_anomaly, score, message, query_time = anomaly_detector.detect_anomaly(point, n_neighbors=n_neighbors)

print('brute   : point {}: is_anomaly={}, score={}, message={}, query time={:.5f}s'.format(point, is_anomaly, score, message,
                                                                                 query_time))