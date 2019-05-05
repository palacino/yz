from noise import pnoise1
from enum import Enum, unique
import random


class FeatureGenerator:
    @unique
    class NoiseType(Enum):
        UNIFORM = 0
        PERLIN = 1

    @staticmethod
    def generate(noise_type, n, scale=1):
        if not isinstance(noise_type, FeatureGenerator.NoiseType):
            if isinstance(noise_type, str):
                noise_type = FeatureGenerator.string2type(noise_type)
            else:
                raise Exception('invalid noise type')
        if noise_type == FeatureGenerator.NoiseType.UNIFORM:
            return [random.random() for i in range(n)]
        elif noise_type == FeatureGenerator.NoiseType.PERLIN:
            offset = random.random()
            return [pnoise1(i / scale + offset + 10, octaves=4) for i in range(n)]

    @staticmethod
    def string2type(noise_string):
        if isinstance(noise_string, str):
            processed_string = noise_string.lower()
            if processed_string == 'uniform':
                return FeatureGenerator.NoiseType.UNIFORM
            elif processed_string == 'perlin':
                return FeatureGenerator.NoiseType.PERLIN
            else:
                raise Exception('invalid noise type: {s}'.format(noise_string))
        else:
            raise Exception('noise_string is not a string')
