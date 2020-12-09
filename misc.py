import atexit
import line_profiler  # use `pip install line-profiler`
from random import random

profile = line_profiler.LineProfiler()  # use as decorator to save line by line timings
# atexit.register(profile.print_stats)


def fast_shuffled(l):
    """This shuffle is about 4x faster than random.shuffle"""
    return sorted(l, key=lambda _: random())


class Party:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class SimulationData:
    def __init__(self, score, num_swaps, time_length):
        self.score = score
        self.num_swaps = num_swaps
        self.time_length = time_length


BLUE = Party('blue', '#5868aa')
RED = Party('red', '#f95955')
TIE = Party('tie', 'black')
