import numpy as np


class InputProcessor:

    @staticmethod
    def build_point_list_from_json(json_object):
        if 'points' in json_object:
            n_points = len(json_object['points'])
            point_data = np.zeros((n_points, 2))
            for i in range(n_points):
                point_data[i, 0] = json_object['points'][i]['x']
                point_data[i, 1] = json_object['points'][i]['y']
        else:
            point_data = np.zeros((1, 2))
            point_data[0, 0] = json_object['x']
            point_data[0, 1] = json_object['y']

        return point_data
