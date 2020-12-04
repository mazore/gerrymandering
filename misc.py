import atexit
import line_profiler  # use `pip install line-profiler`

profile = line_profiler.LineProfiler()
# atexit.register(profile.print_stats)
