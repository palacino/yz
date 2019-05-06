from api.anomaly.neighborfinder import NeighborFinder
import pandas as pd
import numpy as np
import time
import math


class KNNAnomalyDetector:
    def __init__(self, ref_file_path, search_type='mykdtree'):
        try:
            self.__data = np.array(pd.read_csv(ref_file_path, skip_blank_lines=True, header=None))
            self.__neighbor_finder = NeighborFinder(self.__data, search_type)

        except Exception as e:
            print('Could not initialize anomaly detector: {}'.format(e))
            raise e

    def data(self):
        return self.__data

    def check_list(self, points, n_neighbors=10, threshold=0.5):
        n_points, _ = points.shape
        is_anomaly_results = np.zeros(n_points)
        score_results = np.zeros(n_points)
        query_time_results = np.zeros(n_points)
        message_results = [''] * n_points

        for i in range(n_points):
            is_anomaly, score, message, query_time = self.detect_anomaly(points[i], n_neighbors, threshold)
            is_anomaly_results[i] = is_anomaly
            score_results[i] = score
            query_time_results[i] = query_time
            message_results[i] = message

        return is_anomaly_results, score_results, message_results, query_time_results

    def detect_anomaly(self, point, n_neighbors=10, threshold=0.5):

        is_anomaly = -1
        score = math.inf
        message = ''

        start_time = time.time()
        try:
            distance_to_neighbors = self.__neighbor_finder.find_neighbors(point, n_neighbors)
            score = np.mean(distance_to_neighbors)
            if score > threshold:
                is_anomaly = 1
            else:
                is_anomaly = 0
        except Exception as e:
            message = 'something went wrong: {}'.format(e)

        end_time = time.time()
        query_time = end_time - start_time

        return is_anomaly, score, message, query_time
