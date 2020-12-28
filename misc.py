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
    """Pass in a list of [(item, weight), ...], from https://stackoverflow.com/a/3679747/12977120"""
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    n = 0
    for c, w in choices:
        n += w
        if n >= r:
            return c
