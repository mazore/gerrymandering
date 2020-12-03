import atexit
import line_profiler
from parameters import OUTPUT_PROFILER

profile = line_profiler.LineProfiler()
if OUTPUT_PROFILER:
    atexit.register(profile.print_stats)
