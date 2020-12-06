import line_profiler  # use `pip install line-profiler`
from random import random

profile = line_profiler.LineProfiler()  # use as decorator to save line by line timings


def fast_shuffle(l):
    """This shuffle is about 4x faster than random.shuffle"""
    return sorted(l, key=lambda _: random())
