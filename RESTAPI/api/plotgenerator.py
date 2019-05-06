import uuid
from pathlib import Path
import matplotlib.pyplot as plt


class PlotGenerator:
    def __init__(self, app_static_folder):
        self.__static_folder = Path(app_static_folder)

    def __create_image_name(self):
        unique_file_name = Path('temp/' + uuid.uuid4().hex + '.jpg')
        absolute_path = self.__static_folder.joinpath(unique_file_name)
        return unique_file_name, absolute_path

    def generate_demo(self):
        unique_file_name, absolute_path = self.__create_image_name()
        plt.figure()
        plt.plot([1, 2])
        plt.savefig(absolute_path)
        return unique_file_name, 'demo plot', 'this is a demo plot caption'

    def generate_plot(self, data, title, caption):
        unique_file_name, absolute_path = self.__create_image_name()
        plt.figure()
        plt.plot(data)
        plt.savefig(absolute_path)
        return unique_file_name, title, caption

    def generate_anomaly_plot(self, data, points, is_anomaly, scores):
        unique_file_name, absolute_path = self.__create_image_name()
        print('writing image in {}'.format(absolute_path))
        marker_sizes = 1000.0 * scores ** 2
        is_red = is_anomaly == 1
        is_green = is_anomaly == 0

        plt.figure(facecolor='white', figsize=(6, 4))
        plt.scatter(data[:, 0], data[:, 1], c='grey', marker='o', alpha=0.3);

        if is_red.sum() > 0:
            plt.scatter(points[is_red, 0], points[is_red, 1], c='red', s=marker_sizes[is_red], marker='o', alpha=0.2)
            plt.scatter(points[is_red, 0], points[is_red, 1], c='red', marker='o', alpha=0.5);

        if is_green.sum() > 0:
            plt.scatter(points[is_green, 0], points[is_green, 1], c='green', s=marker_sizes[is_green], marker='o',
                        alpha=0.2)
            plt.scatter(points[is_green, 0], points[is_green, 1], c='green', marker='o', alpha=0.5)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig(absolute_path)

        title = 'Query points vs. reference data'
        caption = '{} point(s) tested, {} anomalies found'.format(points.shape[0], is_anomaly.sum())
        return unique_file_name, title, caption
