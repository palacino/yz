from neighborfinder import NeighborFinder
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

    def detect_anomaly(self, point, n_neighbors=10, threshold=0.5):

        is_anomaly = -1
        score = math.inf
        message = ''

        start_time = time.time()
        try:
            distance_to_neighbors = self.__neighbor_finder.find_neighbors(point, n_neighbors)
            score = np.mean(distance_to_neighbors)
        except Exception as e:
            message = 'something went wrong: {}'.format(e)

        end_time = time.time()
        query_time = end_time - start_time

        return is_anomaly, score, message, query_time
