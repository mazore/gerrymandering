import atexit
from constants import OUTPUT_PROFILER
import line_profiler

profile = line_profiler.LineProfiler()
if OUTPUT_PROFILER:
    atexit.register(profile.print_stats)
