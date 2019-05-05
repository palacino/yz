from noise import pnoise1
from enum import Enum, unique


class FeatureGenerator:
    @unique
    class NoiseType(Enum):
        UNIFORM = 0
        PERLIN = 1

    def __init__(self, noise_type):
        self.__noise_type = noise_type

    def generate(self):
        return -1
        #TODO

    def generate_noise(self):
        return -1
        #TODO