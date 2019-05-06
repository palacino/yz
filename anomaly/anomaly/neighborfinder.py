from mykdtree import MyKDTree
import numpy as np
from scipy.spatial import kdtree


class NeighborFinder:
    def __init__(self, data, search_type='brute-force'):
        self.__data = data
        self.__nr, self.__nc = data.shape
        if search_type == 'brute-force':
            self.__search_type = search_type
        elif search_type == 'kdtree':
            self.__search_type = search_type
            self.__kdtree = kdtree.KDTree(data)
        elif search_type == 'mykdtree':
            self.__search_type = search_type
            self.__kdtree = MyKDTree(data)
        else:
            raise Exception('unknown search type: {}'.format(search_type))

    def find_neighbors(self, point, n=5):
        result = None
        if self.__search_type == 'kdtree':
            result = self.__find_from_kdtree(point, n)
        if self.__search_type == 'mykdtree':
            result = self.__find_from_mykdtree(point, n)
        elif self.__search_type == 'brute-force':
            result = self.__find_brute_force(point, n)
        return result

    def __find_from_kdtree(self, point, n):
        distances = self.__kdtree.query(point, n)
        return distances[0]

    def __find_from_mykdtree(self, point, n):
        distances, node_ids = self.__kdtree.query(point, n)
        return distances

    def __find_brute_force(self, point, n):
        squared_distances = np.zeros(self.__nr)
        for i in range(self.__nr):
            squared_distances[i] = (point[0] - self.__data[i, 0]) ** 2 + (point[1] - self.__data[i, 1]) ** 2

        sorted_sq_distances = np.sort(squared_distances)
        return np.sqrt(sorted_sq_distances[0:n])
