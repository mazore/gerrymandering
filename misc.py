import atexit
import line_profiler  # use `pip install line-profiler`
from random import random

profile = line_profiler.LineProfiler()  # use as decorator to save line by line timings
# atexit.register(profile.print_stats)


def fast_shuffled(l):
    """This shuffle is about 4x faster than random.shuffle"""
    return sorted(l, key=lambda _: random())


class SimulationData:
    def __init__(self, score, num_swaps, time_length):
        self.score = score
        self.num_swaps = num_swaps
        self.time_length = time_length
