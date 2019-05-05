import numpy as np
from featuregenerator import FeatureGenerator


class DatasetCreator:
    @staticmethod
    def create_simple(n, n_timesteps, scale=500):
        result = np.zeros([n, n_timesteps])
        labels = np.zeros([n, 1])
        random_data = FeatureGenerator.generate('perlin', n + n_timesteps, scale)
        for i in range(n):
            result[i, :] = random_data[i:i + n_timesteps]
            labels[i] = random_data[i + n_timesteps]

        return result, labels
