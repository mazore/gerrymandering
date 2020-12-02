import atexit
import line_profiler

profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)
