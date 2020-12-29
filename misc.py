import atexit
from math import inf
from random import random, uniform

try:
    import line_profiler  # use `pip install line-profiler`

    profile = line_profiler.LineProfiler()  # use as decorator to save & print timings
    atexit.register(lambda: profile.print_stats() if profile.functions else None)  # print stats if decorator used
except ImportError as e:
    line_profiler = None
    profile = None


def constrain(val, min_val=-inf, max_val=inf):
    return min(max_val, max(min_val, val))


def fast_shuffled(l):
    """This shuffle is about 4x faster than random.shuffle"""
    return sorted(l, key=lambda _: random())


def hex_to_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def rgb_to_hex(r, g, b):
    r = constrain(r, min_val=0, max_val=255)
    g = constrain(g, min_val=0, max_val=255)
    b = constrain(b, min_val=0, max_val=255)
    return '#%02x%02x%02x' % (r, g, b)


def weighted_choice(choices):
    """Pass in a list of [(item, weight), ...], from https://stackoverflow.com/a/3679747/12977120"""
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    n = 0
    for c, w in choices:
        n += w
        if n >= r:
            return c
