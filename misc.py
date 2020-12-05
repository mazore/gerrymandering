import atexit
import line_profiler  # use `pip install line-profiler`

profile = line_profiler.LineProfiler()  # use as decorator to save line by line timings
# atexit.register(profile.print_stats)  # print profiler result on exit
