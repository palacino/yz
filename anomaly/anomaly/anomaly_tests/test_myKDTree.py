from unittest import TestCase
from mykdtree import MyKDTree
import numpy as np
from scipy.spatial import KDTree


class TestMyKDTree(TestCase):
    def setUp(self) -> None:
        # https://gopalcdas.com/2017/05/24/construction-of-k-d-tree-and-using-it-for-nearest-neighbour-search/
        self.test_data1 = np.array(
            [[1, 3], [1, 8], [2, 2], [2, 10], [3, 6], [4, 1], [5, 4], [6, 8], [7, 4], [7, 7], [8, 2],
             [8, 5], [9, 9]])

        # https://en.wikipedia.org/wiki/K-d_tree
        self.test_data2 = np.array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])

    def test_tree_creation(self):
        tree = MyKDTree(self.test_data2)

        root = tree.root()
        self.assertEqual(root[0], 5, 'incorrect root')
        # left
        self.assertEqual(root[2][0], 1, 'incorrect id')
        # left left
        self.assertEqual(root[2][2][0], 0, 'incorrect id')
        self.assertEqual(root[2][2][2], None, 'node should be leaf')
        self.assertEqual(root[2][2][3], None, 'node should be leaf')
        # left right
        self.assertEqual(root[2][3][0], 3, 'incorrect id')
        self.assertEqual(root[2][3][2], None, 'node should be leaf')
        self.assertEqual(root[2][3][3], None, 'node should be leaf')
        # right
        self.assertEqual(root[3][0], 2, 'incorrect id')
        # right left
        self.assertEqual(root[3][2][0], 4, 'incorrect id')
        self.assertEqual(root[3][2][2], None, 'node should be leaf')
        self.assertEqual(root[3][2][3], None, 'node should be leaf')

        # right right
        self.assertEqual(root[3][3], None, 'no right branch')

        tree = MyKDTree(self.test_data1)
        root = tree.root()
        self.assertEqual(root[0], 6, 'incorrect root')
        self.assertEqual(root[1][0], 5, 'incorrect root x')
        self.assertEqual(root[1][1], 4, 'incorrect root x')

    def test_tree_query(self):
        tree = MyKDTree(self.test_data1)
        test_point = [3, 6]
        distances, ids = tree.query(test_point, 5)
        self.assertEqual(distances.size, 5, 'incorrect number of neighbors')
        self.assertEqual(ids.size, 5, 'incorrect number of neighbors')
        self.assertEqual(distances[0], 0.0, 'point in tree should have zero distance')

    def test_equivalaence_to_scipy_tree(self):
        scipy_tree = KDTree(self.test_data1)
        mytree = MyKDTree(self.test_data1)

        # added decimals to avoid multiple solutions
        test_points = [[-10.1, -10.1], [10.3, 10.2], [1.1, 3.6], [7.1, 6.6]]
        n_neighbors = [2, 3, 4, 5, 6, 7, 8, 9, 10]

        for n in n_neighbors:
            for p in test_points:
                distances_m, ids_m = mytree.query(p, n)
                result_s = scipy_tree.query(p, n)
                distances_s = result_s[0]
                ids_s = result_s[1]
                for i in range(n):
                    self.assertEqual(distances_m[i], distances_s[i], 'distances to nearest neighbors should be equal')
                    self.assertEqual(ids_m[i], ids_s[i], 'node ids should be equal')
