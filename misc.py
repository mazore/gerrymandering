import atexit
from parameters import OUTPUT_PROFILER

if OUTPUT_PROFILER:
    import line_profiler
    profile = line_profiler.LineProfiler()
    atexit.register(profile.print_stats)
