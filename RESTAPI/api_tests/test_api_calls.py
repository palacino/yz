from unittest import TestCase
import api
from flask import json


class TestAPICalls(TestCase):

    def setUp(self):
        self.app = api.create_app('config.Test', testing=True)
        self.client = self.app.test_client()
        self.json_single_point_no_anomaly = {'x': 3.0, 'y': 2.2}
        self.json_single_point_anomaly = {'x': 8.0, 'y': 8.2}
        self.json_multiple_points = {'points': [{'x': 2.0, 'y': 3.0}, {'x': 4.0, 'y': 5.0}]}

    def test_hello_world(self):
        result = self.client.get('/')

        self.assertIsNotNone(result, 'no response')
        self.assertEqual(result.status_code, 200, 'status code is not 200')
        self.assertEqual(result.data, b'Hello world from Flask!', 'incorrect text')

    def test_check_get_should_return_a_value(self):
        result = self.client.get('/check?x=3.0&y=2.5')

        json_object = result.get_json()
        self.assertIsNotNone(json_object, 'result should contain json')

    def test_check_get_should_detect_no_anomaly(self):
        result = self.client.get('/check?x=3.0&y=2.5')

        json_object = result.get_json()
        self.assertEqual(0, json_object['is_anomaly'], 'result should be a good value')

    def test_check_get_should_detect_an_anomaly(self):
        result = self.client.get('/check?x=30.0&y=2.5')

        json_object = result.get_json()
        self.assertEqual(1, json_object['is_anomaly'], 'result should be a good value')

    def test_check_post_should_detect_an_anomaly(self):
        result = self.client.post('/check', json=self.json_single_point_anomaly)

        json_object = result.get_json()
        self.assertEqual(1, json_object['is_anomaly'][0], 'result should be a good value')

    def test_check_post_should_detect_a_good_value(self):
        result = self.client.post('/check', json=self.json_single_point_no_anomaly)

        json_object = result.get_json()
        self.assertEqual(0, json_object['is_anomaly'][0], 'result should be a good value')

    def test_check_post_multiple_values_should_return_multiple_results(self):
        result = self.client.post('/check', json=self.json_multiple_points)

        json_object = result.get_json()
        self.assertEqual(len(json_object['is_anomaly']), 2, 'should have two results')

    def test_check_post_multiple_values_should_detect_correct_anomaly_status(self):
        result = self.client.post('/check', json=self.json_multiple_points)

        json_object = result.get_json()
        self.assertEqual(json_object['is_anomaly'][0], 1, 'first point should be anomaly')
        self.assertEqual(json_object['is_anomaly'][1], 0, 'second point should be normal')
