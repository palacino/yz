import uuid
from pathlib import Path
import matplotlib.pyplot as plt


class PlotGenerator:
    def __init__(self, app_root_folder):
        self.__static_folder = Path(app_root_folder).joinpath(Path('static'))

    def generate_demo(self):
        unique_file_name = Path('temp/' + uuid.uuid4().hex + '.jpg')
        absolute_path = self.__static_folder.joinpath(unique_file_name)
        plt.figure()
        plt.plot([1, 2])
        plt.savefig(absolute_path)
        return unique_file_name, 'demo plot', 'this is a demo plot caption'

    def generate_plot(self, data, title, caption):
        unique_file_name = Path('temp/' + uuid.uuid4().hex + '.jpg')
        absolute_path = self.__static_folder.joinpath(unique_file_name)
        plt.figure()
        plt.plot(data)
        plt.savefig(absolute_path)
        return unique_file_name, title, caption
