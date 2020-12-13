import atexit
from random import random, uniform

try:
    import line_profiler  # use `pip install line-profiler`
    profile = line_profiler.LineProfiler()  # use as decorator to save & print timings
    atexit.register(lambda: profile.print_stats() if profile.functions else None)  # print stats if decorator used
except ImportError as e:
    line_profiler = None
    profile = None


def fast_shuffled(l):
    """This shuffle is about 4x faster than random.shuffle"""
    return sorted(l, key=lambda _: random())


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    n = 0
    for c, w in choices:
        n += w
        if n >= r:
            return c


class Party:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class SimulationData:
    def __init__(self, score, num_swaps, total_time, total_swap_time):
        self.score = score
        self.num_swaps = num_swaps
        self.total_time = total_time
        self.total_swap_time = total_swap_time


BLUE = Party('blue', '#5868aa')
RED = Party('red', '#f95955')
TIE = Party('tie', 'black')
