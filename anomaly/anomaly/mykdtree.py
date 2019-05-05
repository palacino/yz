from scipy.spatial import distance
import math
import heapq
import numpy as np


# following algorithm description in
# https://gopalcdas.com/2017/05/24/construction-of-k-d-tree-and-using-it-for-nearest-neighbour-search/

class MyKDTree:
    def __init__(self, data):
        self.__nr, self.__nc = data.shape
        all_indices = np.array(range(self.__nr))
        self.__root = self.__build_tree(data, all_indices, 0)

    # Build the tree recursively, each time splitting the remaining data according to the median value
    # found in a different dimension. We keep track of the ids of the data points (indices).
    def __build_tree(self, data, real_indices, depth):
        if data.size == 0:
            return None

        nr, nc = data.shape
        dimension = depth % nc

        values_to_sort = data[:, dimension]
        sorted_indices = np.argsort(values_to_sort)
        median_index = nr // 2

        real_median_index = real_indices[sorted_indices[median_index]]
        left_selection = sorted_indices[0:median_index]
        right_selection = sorted_indices[median_index + 1:]

        left = self.__build_tree(data[left_selection, :], real_indices[left_selection], depth + 1)
        right = self.__build_tree(data[right_selection, :], real_indices[right_selection], depth + 1)

        return real_median_index, data[sorted_indices[median_index], :], left, right, depth

    # Query the tree to find the closest n neighbors. Here we use a priority queue (a heap) to keep track of
    # the closes n points during the recursive process
    def query(self, point, n=5):
        if n > self.__nr:
            n = self.__nr
        priority_queue = []
        for i in range(n):
            heapq.heappush(priority_queue, (math.inf, None))
        self.__query_node(priority_queue, math.inf, point, self.__root, n)
        nearest_neighbors = heapq.nsmallest(n, priority_queue)
        distances = np.zeros(n)
        node_ids = np.zeros(n)
        for i in range(n):
            distances[i] = math.sqrt(nearest_neighbors[i][0])
            node_ids[i] = nearest_neighbors[i][1][0]

        return [distances, node_ids]

    # The main recursive procedure.
    def __query_node(self, priority_queue, n_smallest, point, node, n):
        if not node:
            return n_smallest
        node_location = node[1]
        dimension = node[4] % self.__nc
        left = node[2]
        right = node[3]
        distance_to_splitting_plane = self.__distance_to_splitting_plane(point, node_location, dimension)

        # do left and right? do smallest first
        if abs(distance_to_splitting_plane) > n_smallest:
            if distance_to_splitting_plane < 0:
                n_smallest = self.__query_node(priority_queue, n_smallest, point, left, n)
            else:
                n_smallest = self.__query_node(priority_queue, n_smallest, point, right, n)
        else:
            distance_to_node_sq = self.__distance_to_node_sq(point, node_location)
            if distance_to_node_sq < n_smallest:
                heapq.heappush(priority_queue, (distance_to_node_sq, node))
                closest_n_neighbors = heapq.nsmallest(n, priority_queue)
                n_smallest = closest_n_neighbors[n - 1][0]

            if distance_to_splitting_plane < 0:
                n_smallest = self.__query_node(priority_queue, n_smallest, point, left, n)
                n_smallest = self.__query_node(priority_queue, n_smallest, point, right, n)
            else:
                n_smallest = self.__query_node(priority_queue, n_smallest, point, right, n)
                n_smallest = self.__query_node(priority_queue, n_smallest, point, left, n)

        return n_smallest

    @staticmethod
    def __distance_to_splitting_plane(point, node_location, dimension):
        return point[dimension] - node_location[dimension]

    @staticmethod
    def __distance_to_node_sq(point, node_location):
        return distance.sqeuclidean(point, node_location)

    def __str__(self):
        return self.__build_string(self.__root)

    def __build_string(self, node):
        if not node:
            return ''
        root_str = '{} node {} {}\n'.format(' ' * node[4] * 3, node[0], node[1])
        left_str = self.__build_string(node[2])
        right_str = self.__build_string(node[3])
        return root_str + left_str + right_str
