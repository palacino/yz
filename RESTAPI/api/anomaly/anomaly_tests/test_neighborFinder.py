from unittest import TestCase
from api.anomaly.neighborfinder import NeighborFinder
import pandas as pd
import numpy as np


class TestNeighborFinder(TestCase):
    def setUp(self) -> None:
        self.data = np.array(pd.read_csv('../../../../data/anomaly.csv', skip_blank_lines=True, header=None))
        self.neighbor_finder_brute_force = NeighborFinder(self.data, search_type='brute-force')
        self.neighbor_finder_kdtree = NeighborFinder(self.data, search_type='kdtree')
        self.neighbor_finder_mykdtree = NeighborFinder(self.data, search_type='mykdtree')
        self.test_point = [2.0, 2.0]

    def test_number_of_returned_neighbors(self):
        n_neighbors = [1, 5, 10, 20, 50]

        for n in n_neighbors:
            neighbors_brute_force = self.neighbor_finder_brute_force.find_neighbors(self.test_point, n)
            neighbors_kdtree = self.neighbor_finder_kdtree.find_neighbors(self.test_point, n)
            neighbors_mykdtree = self.neighbor_finder_mykdtree.find_neighbors(self.test_point, n)

            self.assertEqual(neighbors_brute_force.size, n, 'incorrect number of neighbors')
            self.assertEqual(neighbors_kdtree.size, n, 'incorrect number of neighbors')
            self.assertEqual(neighbors_mykdtree.size, n, 'incorrect number of neighbors')

    def test_method_equivalence(self):
        n = 5
        neighbors_brute_force = self.neighbor_finder_brute_force.find_neighbors(self.test_point, n)
        neighbors_kdtree = self.neighbor_finder_kdtree.find_neighbors(self.test_point, n)
        neighbors_mykdtree = self.neighbor_finder_mykdtree.find_neighbors(self.test_point, n)

        for i in range(n):
            self.assertEqual(neighbors_brute_force[i], neighbors_kdtree[i], 'methods should produces identical results')
            self.assertEqual(neighbors_brute_force[i], neighbors_mykdtree[i],
                             'methods should produces identical results')
