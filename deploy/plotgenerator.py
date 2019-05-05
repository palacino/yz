import uuid
import pathlib


class PlotGenerator:
    def __init__(self, plot_folder):
        __plot_folder = pathlib.norm_path(plot_folder)

    def generate_demo(self):
        unique_file_name = pathlib.join(self.__plot_folder, uuid.uuid4() + '.jpg')
        print(unique_file_name)

        return unique_file_name
