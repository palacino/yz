from unittest import TestCase
from api.anomaly.knnanomalydetector import KNNAnomalyDetector
import numpy as np
import math


class TestKNNAnomalyDetector(TestCase):
    def setUp(self) -> None:
        self.detector = KNNAnomalyDetector('../../../../data/anomaly.csv', search_type='mykdtree')
        self.single_point = np.array([[2, 3]])
        self.multiple_points = np.array([[2, 3], [4, 5]])
        self.anomaly = np.array([[10, 10]])
        self.no_anomaly = np.array([[2, 2]])

    def test_check_list_for_single_point(self):
        is_anomaly_results, score_results, message_results, query_time_results = self.detector.check_list(
            self.single_point)

        self.assertEqual(is_anomaly_results.shape, (1,), 'incorrect output size')
        self.assertEqual(score_results.shape, (1,), 'incorrect output size')
        self.assertEqual(len(message_results), 1, 'incorrect output size')
        self.assertEqual(query_time_results.shape, (1,), 'incorrect output size')

        self.assertNotEqual(is_anomaly_results[0], -1, 'undetermined anomaly status')
        self.assertNotEqual(score_results[0], math.inf, 'infinite anomaly score')
        self.assertEqual(message_results[0], '', 'message string should be empty')

    def test_check_list_for_multiple_points(self):
        is_anomaly_results, score_results, message_results, query_time_results = self.detector.check_list(
            self.multiple_points)

        self.assertEqual(is_anomaly_results.shape, (2,), 'incorrect output size')
        self.assertEqual(score_results.shape, (2,), 'incorrect output size')
        self.assertEqual(len(message_results), 2, 'incorrect output size')
        self.assertEqual(query_time_results.shape, (2,), 'incorrect output size')

        for i in range(2):
            self.assertNotEqual(is_anomaly_results[i], -1, 'undetermined anomaly status')
            self.assertNotEqual(score_results[i], math.inf, 'infinite anomaly score')
            self.assertEqual(message_results[i], '', 'message string should be empty')

    def test_anomaly_detection(self):
        is_anomaly_r, scores_r, messages_r, query_time_r = self.detector.check_list(self.anomaly)
        is_anomaly_w, scores_w, messages_w, query_time_w = self.detector.check_list(self.no_anomaly)

        self.assertGreater(scores_r[0], scores_w[0], 'anomaly should have larger score than normal point')
        self.assertEqual(is_anomaly_r[0], 1, 'real anomaly not detected')
        self.assertEqual(is_anomaly_w[0], 0, 'normal point not detected')

    def test_speed(self):
        is_anomaly_r, scores_r, messages_r, query_time_r = self.detector.check_list(self.anomaly)

        self.assertLess(query_time_r[0], 0.01, 'detection should be faster than 0.01s')
