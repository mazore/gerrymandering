import atexit
try:
    import line_profiler  # use `pip install line-profiler`
except ImportError as e:
    line_profiler = None
from random import random

if line_profiler is not None:
    profile = line_profiler.LineProfiler()  # use as decorator to save & print timings
    atexit.register(lambda: profile.print_stats() if profile.functions else None)  # print stats if decorator used
else:
    profile = None


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
    def __init__(self, score, num_swaps, total_swap_time):
        self.score = score
        self.num_swaps = num_swaps
        self.total_swap_time = total_swap_time


BLUE = Party('blue', '#5868aa')
RED = Party('red', '#f95955')
TIE = Party('tie', 'black')
