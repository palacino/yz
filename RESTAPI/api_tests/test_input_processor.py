from unittest import TestCase
from api.inputprocessor import InputProcessor
from flask import json


class TestInputProcessor(TestCase):
    def setUp(self) -> None:
        self.single_point_json = """  
        {
            "x": 2.0,
            "y": 3.0
        }"""
        self.multi_point_json = """
        {
            "points": [
                {
                    "x": 2,
                    "y": 3
                },
                {
                    "x": 4,
                    "y": 5
                }
            ]
        }"""

    def test_build_single_point_from_json(self):
        json_object = json.loads(self.single_point_json)
        points = InputProcessor.build_point_list_from_json(json_object)
        self.assertEqual(points.shape, (1, 2), 'wrong size of point list')
        self.assertEqual(points[0, 0], 2.0, 'wrong value for x')
        self.assertEqual(points[0, 1], 3.0, 'wrong value for y')

    def test_build_multi_point_from_json(self):
        json_object = json.loads(self.multi_point_json)
        points = InputProcessor.build_point_list_from_json(json_object)
        self.assertEqual(points.shape, (2, 2), 'wrong size of point list')
        self.assertEqual(points[0, 0], 2.0, 'wrong value for x')
        self.assertEqual(points[0, 1], 3.0, 'wrong value for y')
        self.assertEqual(points[1, 0], 4.0, 'wrong value for x')
        self.assertEqual(points[1, 1], 5.0, 'wrong value for y')
